import json
import time
import urllib.error
import urllib.parse
import urllib.request

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.text import slugify

from exercises.models import Exercise


WIKI_API = "https://en.wikipedia.org/w/api.php"
WIKI_SUMMARY = "https://en.wikipedia.org/api/rest_v1/page/summary/{title}"


def _fetch_json(url: str, *, timeout: int = 15, retries: int = 3) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "GymTracker/1.0 (exercise image fetcher; contact: local-dev)",
            "Accept": "application/json",
        },
        method="GET",
    )

    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
            return json.loads(raw.decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                retry_after = e.headers.get("Retry-After")
                wait_s = float(retry_after) if retry_after else 2.0
                time.sleep(wait_s * (attempt + 1))
                continue
            raise

    # Last attempt without swallowing errors
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
    return json.loads(raw.decode("utf-8"))


def _search_title(term: str) -> str | None:
    qs = urllib.parse.urlencode(
        {
            "action": "query",
            "list": "search",
            "format": "json",
            "srlimit": 1,
            "srsearch": term,
        }
    )
    data = _fetch_json(f"{WIKI_API}?{qs}")
    results = data.get("query", {}).get("search", [])
    if not results:
        return None
    return results[0].get("title")


def _summary(title: str) -> dict | None:
    safe = urllib.parse.quote(title.replace(" ", "_"))
    try:
        return _fetch_json(WIKI_SUMMARY.format(title=safe))
    except Exception:
        return None


def _pick_image_urls(summary: dict) -> tuple[str | None, str | None, str | None]:
    original = summary.get("originalimage", {}).get("source")
    thumb = summary.get("thumbnail", {}).get("source")
    page = (
        summary.get("content_urls", {})
        .get("desktop", {})
        .get("page")
        or summary.get("content_urls", {}).get("mobile", {}).get("page")
    )
    return original, thumb, page


def _download_bytes(
    url: str, *, max_bytes: int, timeout: int = 20, retries: int = 3
) -> tuple[bytes, str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "GymTracker/1.0 (exercise image fetcher; contact: local-dev)",
            "Accept": "image/*",
        },
        method="GET",
    )

    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                content_type = resp.headers.get("Content-Type", "")
                chunks: list[bytes] = []
                total = 0
                while True:
                    chunk = resp.read(64 * 1024)
                    if not chunk:
                        break
                    chunks.append(chunk)
                    total += len(chunk)
                    if total > max_bytes:
                        raise ValueError("Image too large")

            return b"".join(chunks), content_type
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                retry_after = e.headers.get("Retry-After")
                wait_s = float(retry_after) if retry_after else 2.0
                time.sleep(wait_s * (attempt + 1))
                continue
            raise

    raise RuntimeError("Download failed after retries")


def _ext_from(content_type: str, url: str) -> str:
    ct = (content_type or "").split(";")[0].strip().lower()
    if ct in {"image/jpeg", "image/jpg"}:
        return "jpg"
    if ct == "image/png":
        return "png"
    if ct == "image/webp":
        return "webp"

    path = urllib.parse.urlparse(url).path.lower()
    for ext in ("jpg", "jpeg", "png", "webp"):
        if path.endswith(f".{ext}"):
            return "jpg" if ext == "jpeg" else ext
    return "jpg"


class Command(BaseCommand):
    help = "Download and attach images to Exercise.image using Wikipedia thumbnails (Wikimedia-hosted)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Re-download and overwrite images even if Exercise.image already exists.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Max exercises to process (0 = no limit).",
        )
        parser.add_argument(
            "--sleep",
            type=float,
            default=1.0,
            help="Sleep between exercises to be gentle on the API.",
        )
        parser.add_argument(
            "--query-suffix",
            type=str,
            default=" exercise",
            help="Suffix appended to the search query (improves relevance).",
        )

    def handle(self, *args, **options):
        force: bool = options["force"]
        limit: int = options["limit"]
        sleep_s: float = options["sleep"]
        suffix: str = options["query_suffix"]

        max_bytes = int(getattr(settings, "MAX_UPLOAD_SIZE_MB", 5)) * 1024 * 1024

        qs = Exercise.objects.all().order_by("id")
        if not force:
            qs = qs.filter(Q(image__isnull=True) | Q(image=""))

        total = qs.count()
        if limit:
            qs = qs[:limit]

        processed = 0
        attached = 0
        skipped = 0

        self.stdout.write(self.style.MIGRATE_HEADING(f"Fetching images for {total} exercises…"))

        for ex in qs:
            processed += 1

            if ex.image and not force:
                skipped += 1
                continue

            term = f"{ex.name}{suffix}".strip()

            title = ex.name
            summary = _summary(title)
            if not summary or summary.get("type") == "https://mediawiki.org/wiki/HyperSwitch/errors/not_found":
                found = _search_title(term)
                if found:
                    summary = _summary(found)

            if not summary:
                self.stdout.write(self.style.WARNING(f"⊘ No page found for: {ex.name}"))
                continue

            original_url, thumb_url, _page = _pick_image_urls(summary)
            if not (original_url or thumb_url):
                self.stdout.write(self.style.WARNING(f"⊘ No image available for: {ex.name}"))
                continue

            image_url = original_url or thumb_url
            try:
                data, content_type = _download_bytes(image_url, max_bytes=max_bytes)
            except ValueError:
                # Original too big: fallback to thumbnail when available.
                if thumb_url and thumb_url != image_url:
                    try:
                        image_url = thumb_url
                        data, content_type = _download_bytes(image_url, max_bytes=max_bytes)
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"⊘ Failed download for {ex.name}: {e}"))
                        continue
                else:
                    self.stdout.write(self.style.WARNING(f"⊘ Image too large for: {ex.name}"))
                    continue
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"⊘ Failed download for {ex.name}: {e}"))
                continue

            ext = _ext_from(content_type, image_url)
            filename = f"{slugify(ex.name) or 'exercise'}.{ext}"

            try:
                ex.image.save(filename, ContentFile(data), save=True)
                attached += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Attached image: {ex.name}"))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"⊘ Failed attach for {ex.name}: {e}"))

            if sleep_s:
                time.sleep(sleep_s)

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone. Processed={processed}, attached={attached}, skipped={skipped}."
            )
        )
