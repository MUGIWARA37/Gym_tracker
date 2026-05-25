from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from exercises.models import Exercise
from notifications.models import Notification
from nutrition.models import NutritionGoal
from progress.models import ProgressEntry
from sessions.models import ExerciseLog, WorkoutSession
from users.models import User
from workouts.models import WorkoutPlan, WorkoutPlanExercise


class Command(BaseCommand):
    help = "Seed demo data for all existing pages."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            default="demo",
            help="Username for the seeded account.",
        )
        parser.add_argument(
            "--email",
            default="demo@example.com",
            help="Email for the seeded account.",
        )
        parser.add_argument(
            "--password",
            default="DemoPass123!",
            help="Password for the seeded account.",
        )

    def handle(self, *args, **options):
        username = options["username"]
        email = options["email"]
        password = options["password"]

        with transaction.atomic():
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "role": "user",
                    "fitness_goal": "build_muscle",
                    "age": 28,
                    "height_cm": 178,
                    "weight_kg": 78,
                },
            )
            if not created:
                user.email = email
                user.fitness_goal = user.fitness_goal or "build_muscle"
            user.set_password(password)
            user.save()

            exercises = list(
                Exercise.objects.filter(created_by=user).order_by("name")[:4]
            )
            if not exercises:
                exercise_payloads = [
                    {
                        "name": "Barbell Bench Press",
                        "description": "Classic chest press movement.",
                        "muscle_group": "chest",
                        "equipment_needed": "Barbell, bench",
                        "difficulty_level": "intermediate",
                        "calories_burn_estimate": 240,
                        "met_value": 6.0,
                    },
                    {
                        "name": "Pull-Ups",
                        "description": "Bodyweight back exercise.",
                        "muscle_group": "back",
                        "equipment_needed": "Pull-up bar",
                        "difficulty_level": "advanced",
                        "calories_burn_estimate": 260,
                        "met_value": 7.0,
                    },
                    {
                        "name": "Goblet Squat",
                        "description": "Lower-body strength builder.",
                        "muscle_group": "legs",
                        "equipment_needed": "Dumbbell",
                        "difficulty_level": "beginner",
                        "calories_burn_estimate": 220,
                        "met_value": 5.5,
                    },
                    {
                        "name": "Plank",
                        "description": "Core stability hold.",
                        "muscle_group": "core",
                        "equipment_needed": "",
                        "difficulty_level": "beginner",
                        "calories_burn_estimate": 120,
                        "met_value": 3.5,
                    },
                ]
                exercises = [
                    Exercise.objects.create(created_by=user, **payload)
                    for payload in exercise_payloads
                ]

            plan = WorkoutPlan.objects.filter(created_by=user).first()
            if not plan:
                plan = WorkoutPlan.objects.create(
                    title="Strength Starter",
                    description="Balanced full-body strength session.",
                    goal="build_muscle",
                    difficulty="intermediate",
                    estimated_duration=60,
                    created_by=user,
                    is_public=False,
                )
                for index, exercise in enumerate(exercises, start=1):
                    WorkoutPlanExercise.objects.create(
                        plan=plan,
                        exercise=exercise,
                        order=index,
                        sets=3,
                        reps=10 if exercise.muscle_group != "core" else 30,
                        rest_time_seconds=90,
                    )

            if not NutritionGoal.objects.filter(user=user).exists():
                NutritionGoal.objects.create(
                    user=user,
                    calories_target=2400,
                    protein_g=160,
                    carbs_g=250,
                    fats_g=70,
                    water_ml=2500,
                )

            if not ProgressEntry.objects.filter(user=user).exists():
                ProgressEntry.objects.create(
                    user=user,
                    weight_kg=78.0,
                    body_fat_percentage=18.5,
                    chest_cm=98.0,
                    waist_cm=82.0,
                    arm_cm=34.0,
                    leg_cm=56.0,
                )
                ProgressEntry.objects.create(
                    user=user,
                    weight_kg=77.2,
                    body_fat_percentage=18.1,
                    chest_cm=98.5,
                    waist_cm=81.5,
                    arm_cm=34.5,
                    leg_cm=56.5,
                )

            if not WorkoutSession.objects.filter(user=user).exists():
                start_time = timezone.now() - timedelta(days=1, hours=1)
                end_time = start_time + timedelta(hours=1)
                session = WorkoutSession.objects.create(
                    user=user,
                    workout_plan=plan,
                    start_time=start_time,
                    end_time=end_time,
                    calories_burned=520,
                    notes="Felt strong on compound lifts.",
                    mood="motivated",
                    completed=True,
                )
                for exercise in exercises:
                    ExerciseLog.objects.create(
                        session=session,
                        exercise=exercise,
                        sets=3,
                        reps=10 if exercise.muscle_group != "core" else 30,
                        weight_used_kg=40 if exercise.muscle_group != "core" else 0,
                        duration_seconds=60 if exercise.muscle_group == "core" else 0,
                        rest_time_seconds=90,
                        completed=True,
                    )

            if not Notification.objects.filter(user=user).exists():
                Notification.objects.create(
                    user=user,
                    title="Session logged",
                    message="Great work finishing your Strength Starter plan.",
                    type="workout",
                )
                Notification.objects.create(
                    user=user,
                    title="Hydration check",
                    message="Remember to hit your 2.5L water goal today.",
                    type="reminder",
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded demo data for '{username}' (email: {email})."
            )
        )
