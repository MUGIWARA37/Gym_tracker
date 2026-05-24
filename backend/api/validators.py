import os
import uuid

from django.core.exceptions import ValidationError

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"]


def validate_image_upload(file, max_upload_mb):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise ValidationError(f"Unsupported type: {file.content_type}")
    if file.size > max_upload_mb * 1024 * 1024:
        raise ValidationError(f"File too large. Max {max_upload_mb}MB.")
    ext = os.path.splitext(file.name)[1].lower()
    safe_name = f"{uuid.uuid4()}{ext}"
    file.name = safe_name
    return file
