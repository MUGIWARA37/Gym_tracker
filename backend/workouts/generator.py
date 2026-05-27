from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable

from django.db import transaction

from exercises.models import Exercise
from workouts.models import WorkoutPlan, WorkoutPlanExercise


@dataclass(frozen=True)
class ExerciseTemplate:
    name: str
    muscle_group: str
    equipment: str
    difficulty: str
    calories_30m: int = 180
    met: Decimal = Decimal("6.0")


# Minimal curated library. We upsert these into the DB if missing.
EXERCISES: list[ExerciseTemplate] = [
    # Chest
    ExerciseTemplate("Bench Press", "chest", "Barbell", "intermediate"),
    ExerciseTemplate("Incline Dumbbell Press", "chest", "Dumbbells", "beginner"),
    ExerciseTemplate("Push-Up", "chest", "Bodyweight", "beginner"),
    ExerciseTemplate("Cable Fly", "chest", "Cable machine", "intermediate"),
    ExerciseTemplate("Machine Chest Press", "chest", "Machine", "beginner"),
    ExerciseTemplate("Decline Bench Press", "chest", "Barbell", "intermediate"),
    ExerciseTemplate("Dumbbell Fly", "chest", "Dumbbells", "beginner"),
    # Back
    ExerciseTemplate("Pull-Up", "back", "Bodyweight", "intermediate"),
    ExerciseTemplate("Lat Pulldown", "back", "Machine", "beginner"),
    ExerciseTemplate("Barbell Row", "back", "Barbell", "intermediate"),
    ExerciseTemplate("Seated Cable Row", "back", "Cable machine", "beginner"),
    ExerciseTemplate("Single-Arm Dumbbell Row", "back", "Dumbbells", "beginner"),
    ExerciseTemplate("Chest-Supported Row", "back", "Machine", "beginner"),
    ExerciseTemplate("Straight-Arm Pulldown", "back", "Cable machine", "beginner"),
    # Legs
    ExerciseTemplate("Back Squat", "legs", "Barbell", "intermediate"),
    ExerciseTemplate("Romanian Deadlift", "legs", "Barbell", "intermediate"),
    ExerciseTemplate("Leg Press", "legs", "Machine", "beginner"),
    ExerciseTemplate("Walking Lunges", "legs", "Dumbbells", "beginner"),
    ExerciseTemplate("Leg Curl", "legs", "Machine", "beginner"),
    ExerciseTemplate("Calf Raise", "legs", "Machine", "beginner"),
    # Shoulders
    ExerciseTemplate("Overhead Press", "shoulders", "Barbell", "intermediate"),
    ExerciseTemplate("Dumbbell Shoulder Press", "shoulders", "Dumbbells", "beginner"),
    ExerciseTemplate("Lateral Raise", "shoulders", "Dumbbells", "beginner"),
    ExerciseTemplate("Face Pull", "shoulders", "Cable machine", "beginner"),
    # Arms
    ExerciseTemplate("Biceps Curl", "arms", "Dumbbells", "beginner"),
    ExerciseTemplate("Triceps Pushdown", "arms", "Cable machine", "beginner"),
    ExerciseTemplate("Dips", "arms", "Bodyweight", "intermediate"),
    # Core
    ExerciseTemplate("Plank", "core", "Bodyweight", "beginner", calories_30m=140, met=Decimal("4.0")),
    ExerciseTemplate("Hanging Knee Raise", "core", "Bodyweight", "intermediate", calories_30m=160, met=Decimal("5.0")),
    ExerciseTemplate("Cable Crunch", "core", "Cable machine", "beginner", calories_30m=150, met=Decimal("4.5")),
    # Full body / conditioning
    ExerciseTemplate("Kettlebell Swing", "full_body", "Kettlebell", "intermediate", calories_30m=260, met=Decimal("8.0")),
    ExerciseTemplate("Jump Rope", "full_body", "Rope", "beginner", calories_30m=300, met=Decimal("10.0")),
    ExerciseTemplate("Burpees", "full_body", "Bodyweight", "intermediate", calories_30m=320, met=Decimal("10.5")),
]


def _upsert_exercise(t: ExerciseTemplate, *, created_by) -> Exercise:
    ex, _created = Exercise.objects.update_or_create(
        name=t.name,
        defaults={
            "description": "",
            "muscle_group": t.muscle_group,
            "equipment_needed": t.equipment,
            "difficulty_level": t.difficulty,
            "calories_burn_estimate": t.calories_30m,
            "met_value": t.met,
            "video_url": "",
            "created_by": created_by,
        },
    )
    return ex


def _split(days: int, goal: str) -> list[dict]:
    # Strength/Hypertrophy: classic splits
    if goal in {"build_muscle", "strength", "maintain"}:
        if days == 4:
            return [
                {"day": 1, "name": "Upper"},
                {"day": 2, "name": "Lower"},
                {"day": 3, "name": "Upper"},
                {"day": 4, "name": "Lower"},
            ]
        if days == 5:
            return [
                {"day": 1, "name": "Push"},
                {"day": 2, "name": "Pull"},
                {"day": 3, "name": "Legs"},
                {"day": 4, "name": "Upper"},
                {"day": 5, "name": "Lower"},
            ]
        return [
            {"day": 1, "name": "Push"},
            {"day": 2, "name": "Pull"},
            {"day": 3, "name": "Legs"},
            {"day": 4, "name": "Push"},
            {"day": 5, "name": "Pull"},
            {"day": 6, "name": "Legs"},
        ]

    # Fat loss / cardio: strength + conditioning cadence
    if days == 4:
        return [
            {"day": 1, "name": "Full Body Strength A"},
            {"day": 2, "name": "Conditioning"},
            {"day": 3, "name": "Full Body Strength B"},
            {"day": 4, "name": "Conditioning"},
        ]
    if days == 5:
        return [
            {"day": 1, "name": "Full Body Strength A"},
            {"day": 2, "name": "Conditioning"},
            {"day": 3, "name": "Full Body Strength B"},
            {"day": 4, "name": "Conditioning"},
            {"day": 5, "name": "Full Body Strength C"},
        ]
    return [
        {"day": 1, "name": "Full Body Strength A"},
        {"day": 2, "name": "Conditioning"},
        {"day": 3, "name": "Full Body Strength B"},
        {"day": 4, "name": "Conditioning"},
        {"day": 5, "name": "Full Body Strength C"},
        {"day": 6, "name": "Conditioning"},
    ]


def _prescription(goal: str, difficulty: str) -> dict:
    # Defaults tuned for a simple, safe generator.
    if goal == "strength":
        if difficulty == "beginner":
            return {"sets": 4, "reps": 5, "rest": 150}
        if difficulty == "intermediate":
            return {"sets": 5, "reps": 4, "rest": 180}
        return {"sets": 5, "reps": 3, "rest": 210}

    if goal in {"lose_weight", "cardio"}:
        if difficulty == "advanced":
            return {"sets": 4, "reps": 15, "rest": 45}
        return {"sets": 3, "reps": 12, "rest": 60}

    # build_muscle / maintain
    if difficulty == "beginner":
        return {"sets": 3, "reps": 10, "rest": 75}
    if difficulty == "intermediate":
        return {"sets": 4, "reps": 10, "rest": 90}
    return {"sets": 4, "reps": 8, "rest": 105}


def _pick(*, muscle_groups: Iterable[str], created_by, difficulty: str) -> list[Exercise]:
    allowed = []
    for t in EXERCISES:
        if t.muscle_group in muscle_groups:
            allowed.append(t)

    # Prefer templates at/below selected difficulty.
    order = {"beginner": 0, "intermediate": 1, "advanced": 2}
    cap = order.get(difficulty, 0)
    allowed = [t for t in allowed if order.get(t.difficulty, 0) <= cap] or allowed

    return [_upsert_exercise(t, created_by=created_by) for t in allowed]


def _day_exercises(day_name: str, *, created_by, goal: str, difficulty: str) -> list[Exercise]:
    dn = day_name.lower()

    if "push" in dn:
        return _pick(muscle_groups=["chest", "shoulders", "arms"], created_by=created_by, difficulty=difficulty)
    if "pull" in dn:
        return _pick(muscle_groups=["back", "shoulders", "arms", "core"], created_by=created_by, difficulty=difficulty)
    if "legs" in dn or "lower" in dn:
        return _pick(muscle_groups=["legs", "core"], created_by=created_by, difficulty=difficulty)
    if "upper" in dn:
        return _pick(muscle_groups=["chest", "back", "shoulders", "arms"], created_by=created_by, difficulty=difficulty)
    if "conditioning" in dn:
        return _pick(muscle_groups=["full_body", "core", "legs"], created_by=created_by, difficulty=difficulty)

    # full body strength
    return _pick(muscle_groups=["full_body", "chest", "back", "legs", "core", "shoulders"], created_by=created_by, difficulty=difficulty)


def _nutrition(days: int, goal: str) -> dict:
    # We don't know bodyweight in the app, so we provide per-kg guidance + calorie deltas.
    # Days/week slightly nudges carb targets for training volume.
    carbs = {4: "3–4", 5: "3.5–4.5", 6: "4–5"}.get(days, "3–4")

    if goal == "lose_weight":
        return {
            "calories": "Maintenance -300 to -500 kcal/day",
            "protein": "1.8–2.2 g/kg/day",
            "carbs": f"{carbs} g/kg/day",
            "fats": "0.6–0.8 g/kg/day",
            "water": "30–40 ml/kg/day",
            "notes": "Prioritize lean protein + high-fiber carbs. Aim 8–10k steps/day.",
        }
    if goal == "build_muscle":
        return {
            "calories": "Maintenance +200 to +350 kcal/day",
            "protein": "1.6–2.2 g/kg/day",
            "carbs": f"{carbs} g/kg/day",
            "fats": "0.8–1.0 g/kg/day",
            "water": "30–40 ml/kg/day",
            "notes": "Hit protein daily and distribute across 3–5 meals. Sleep 7–9h.",
        }
    if goal == "strength":
        return {
            "calories": "Maintenance to +200 kcal/day",
            "protein": "1.6–2.0 g/kg/day",
            "carbs": f"{carbs} g/kg/day",
            "fats": "0.8–1.0 g/kg/day",
            "water": "30–40 ml/kg/day",
            "notes": "Keep carbs higher on heavy days. Rest 2–3 min on compounds.",
        }
    if goal == "cardio":
        return {
            "calories": "Maintenance (or -200 if cutting)",
            "protein": "1.6–2.0 g/kg/day",
            "carbs": f"{carbs} g/kg/day",
            "fats": "0.8–1.0 g/kg/day",
            "water": "35–45 ml/kg/day",
            "notes": "Fuel with carbs around conditioning sessions; add electrolytes if sweating a lot.",
        }

    # maintain
    return {
        "calories": "Maintenance",
        "protein": "1.6–2.0 g/kg/day",
        "carbs": f"{carbs} g/kg/day",
        "fats": "0.8–1.0 g/kg/day",
        "water": "30–40 ml/kg/day",
        "notes": "Stay consistent; aim for progressive overload or maintain performance.",
    }


@transaction.atomic
def generate_plan(plan: WorkoutPlan) -> None:
    # Clear any existing exercises in the plan (safe for regeneration).
    WorkoutPlanExercise.objects.filter(plan=plan).delete()

    split = _split(plan.days_per_week, plan.goal)
    plan.structure = {"split": split}
    plan.nutrition_guidance = _nutrition(plan.days_per_week, plan.goal)
    plan.save(update_fields=["structure", "nutrition_guidance"])

    base = _prescription(plan.goal, plan.difficulty)

    for day_meta in split:
        day = int(day_meta["day"])
        day_name = str(day_meta["name"])

        candidates = _day_exercises(day_name, created_by=plan.created_by, goal=plan.goal, difficulty=plan.difficulty)

        # Pick a stable subset (first N) to keep deterministic results.
        # Conditioning days use fewer movements, strength days a bit more.
        n = 6
        if "conditioning" in day_name.lower():
            n = 5
        chosen = candidates[:n]

        for idx, ex in enumerate(chosen, start=1):
            # Slightly bias core/conditioning to higher reps.
            sets = base["sets"]
            reps = base["reps"]
            rest = base["rest"]

            if plan.goal in {"lose_weight", "cardio"} and ex.muscle_group in {"full_body", "core"}:
                reps = max(reps, 15)
                rest = min(rest, 60)

            WorkoutPlanExercise.objects.create(
                plan=plan,
                day=day,
                exercise=ex,
                order=idx,
                sets=sets,
                reps=reps,
                rest_time_seconds=rest,
            )
