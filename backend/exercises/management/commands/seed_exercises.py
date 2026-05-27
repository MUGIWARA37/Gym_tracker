from django.core.management.base import BaseCommand
from exercises.models import Exercise


class Command(BaseCommand):
    help = "Seed database with common gym exercises"

    def handle(self, *args, **options):
        exercises_data = [
            # CHEST
            {
                "name": "Barbell Bench Press",
                "description": "Classic compound exercise for chest development. Lie on bench, press barbell up from chest level.",
                "muscle_group": "chest",
                "equipment_needed": "Barbell, Bench",
                "difficulty_level": "intermediate",
                "calories_burn_estimate": 180,
                "met_value": 6.0,
            },
            {
                "name": "Dumbbell Chest Press",
                "description": "Press dumbbells up from chest while lying on bench. Great for chest development.",
                "muscle_group": "chest",
                "equipment_needed": "Dumbbells, Bench",
                "difficulty_level": "beginner",
                "calories_burn_estimate": 160,
                "met_value": 5.5,
            },
            {
                "name": "Push-ups",
                "description": "Bodyweight exercise for chest, shoulders, and triceps. Can be modified for any level.",
                "muscle_group": "chest",
                "equipment_needed": "",
                "difficulty_level": "beginner",
                "calories_burn_estimate": 140,
                "met_value": 4.5,
            },
            {
                "name": "Incline Bench Press",
                "description": "Press barbell on inclined bench to target upper chest.",
                "muscle_group": "chest",
                "equipment_needed": "Barbell, Incline Bench",
                "difficulty_level": "intermediate",
                "calories_burn_estimate": 170,
                "met_value": 5.8,
            },
            {
                "name": "Cable Chest Fly",
                "description": "Pull cables in a fly motion to isolate chest muscles.",
                "muscle_group": "chest",
                "equipment_needed": "Cable Machine",
                "difficulty_level": "intermediate",
                "calories_burn_estimate": 120,
                "met_value": 3.8,
            },
            # BACK
            {
                "name": "Barbell Deadlifts",
                "description": "Lift barbell from ground to hip level. Compound exercise for entire back and legs.",
                "muscle_group": "back",
                "equipment_needed": "Barbell",
                "difficulty_level": "advanced",
                "calories_burn_estimate": 220,
                "met_value": 7.5,
            },
            {
                "name": "Lat Pulldowns",
                "description": "Pull cable down in front or behind neck to work lats.",
                "muscle_group": "back",
                "equipment_needed": "Cable Machine",
                "difficulty_level": "beginner",
                "calories_burn_estimate": 140,
                "met_value": 4.5,
            },
            {
                "name": "Bent Over Barbell Rows",
                "description": "Bent over barbell row to strengthen back and biceps.",
                "muscle_group": "back",
                "equipment_needed": "Barbell",
                "difficulty_level": "intermediate",
                "calories_burn_estimate": 200,
                "met_value": 6.8,
            },
            {
                "name": "Pull-ups",
                "description": "Bodyweight exercise that pulls your entire body weight up. Excellent for back and arms.",
                "muscle_group": "back",
                "equipment_needed": "Pull-up Bar",
                "difficulty_level": "intermediate",
                "calories_burn_estimate": 160,
                "met_value": 5.5,
            },
            {
                "name": "Dumbbell Rows",
                "description": "Row dumbbell to hip with one arm to strengthen back.",
                "muscle_group": "back",
                "equipment_needed": "Dumbbell, Bench",
                "difficulty_level": "intermediate",
                "calories_burn_estimate": 150,
                "met_value": 5.0,
            },
            # LEGS
            {
                "name": "Barbell Back Squat",
                "description": "Place barbell on shoulders and squat down. Key compound exercise for leg strength.",
                "muscle_group": "legs",
                "equipment_needed": "Barbell, Squat Rack",
                "difficulty_level": "advanced",
                "calories_burn_estimate": 240,
                "met_value": 8.0,
            },
            {
                "name": "Leg Press",
                "description": "Push weight away using your legs on machine. Good for quad and glute development.",
                "muscle_group": "legs",
                "equipment_needed": "Leg Press Machine",
                "difficulty_level": "beginner",
                "calories_burn_estimate": 180,
                "met_value": 6.0,
            },
            {
                "name": "Dumbbell Lunges",
                "description": "Step forward and lower body with dumbbells in hand.",
                "muscle_group": "legs",
                "equipment_needed": "Dumbbells",
                "difficulty_level": "intermediate",
                "calories_burn_estimate": 160,
                "met_value": 5.5,
            },
            {
                "name": "Leg Curl",
                "description": "Curl legs up on machine to isolate hamstrings.",
                "muscle_group": "legs",
                "equipment_needed": "Leg Curl Machine",
                "difficulty_level": "beginner",
                "calories_burn_estimate": 120,
                "met_value": 3.8,
            },
            {
                "name": "Bulgarian Split Squats",
                "description": "Single leg squat with rear foot elevated on bench.",
                "muscle_group": "legs",
                "equipment_needed": "Bench, Dumbbells",
                "difficulty_level": "intermediate",
                "calories_burn_estimate": 140,
                "met_value": 4.5,
            },
            # SHOULDERS
            {
                "name": "Overhead Press",
                "description": "Press barbell overhead from shoulder height to strengthen shoulders.",
                "muscle_group": "shoulders",
                "equipment_needed": "Barbell",
                "difficulty_level": "intermediate",
                "calories_burn_estimate": 160,
                "met_value": 5.5,
            },
            {
                "name": "Dumbbell Shoulder Press",
                "description": "Press dumbbells overhead from seated position.",
                "muscle_group": "shoulders",
                "equipment_needed": "Dumbbells, Bench",
                "difficulty_level": "intermediate",
                "calories_burn_estimate": 150,
                "met_value": 5.0,
            },
            {
                "name": "Lateral Raises",
                "description": "Raise dumbbells out to sides to target lateral deltoids.",
                "muscle_group": "shoulders",
                "equipment_needed": "Dumbbells",
                "difficulty_level": "beginner",
                "calories_burn_estimate": 100,
                "met_value": 3.0,
            },
            {
                "name": "Machine Shoulder Press",
                "description": "Press weight on machine to strengthen shoulders.",
                "muscle_group": "shoulders",
                "equipment_needed": "Shoulder Press Machine",
                "difficulty_level": "beginner",
                "calories_burn_estimate": 140,
                "met_value": 4.5,
            },
            {
                "name": "Face Pulls",
                "description": "Pull cable to face level to strengthen rear deltoids.",
                "muscle_group": "shoulders",
                "equipment_needed": "Cable Machine",
                "difficulty_level": "beginner",
                "calories_burn_estimate": 110,
                "met_value": 3.2,
            },
            # ARMS
            {
                "name": "Barbell Curls",
                "description": "Curl barbell up to work biceps.",
                "muscle_group": "arms",
                "equipment_needed": "Barbell",
                "difficulty_level": "beginner",
                "calories_burn_estimate": 120,
                "met_value": 3.8,
            },
            {
                "name": "Dumbbell Curls",
                "description": "Curl dumbbells up to strengthen biceps.",
                "muscle_group": "arms",
                "equipment_needed": "Dumbbells",
                "difficulty_level": "beginner",
                "calories_burn_estimate": 110,
                "met_value": 3.5,
            },
            {
                "name": "Tricep Dips",
                "description": "Use bench or bars to lower and raise body. Excellent for triceps.",
                "muscle_group": "arms",
                "equipment_needed": "Dip Bar, Bench",
                "difficulty_level": "intermediate",
                "calories_burn_estimate": 150,
                "met_value": 5.0,
            },
            {
                "name": "Skull Crushers",
                "description": "Lower barbell behind head to work triceps.",
                "muscle_group": "arms",
                "equipment_needed": "Barbell, Bench",
                "difficulty_level": "intermediate",
                "calories_burn_estimate": 130,
                "met_value": 4.2,
            },
            {
                "name": "Cable Tricep Pushdown",
                "description": "Push cable down to isolate triceps.",
                "muscle_group": "arms",
                "equipment_needed": "Cable Machine",
                "difficulty_level": "beginner",
                "calories_burn_estimate": 100,
                "met_value": 3.0,
            },
            # CORE
            {
                "name": "Plank",
                "description": "Hold body in straight line to strengthen core.",
                "muscle_group": "core",
                "equipment_needed": "",
                "difficulty_level": "beginner",
                "calories_burn_estimate": 80,
                "met_value": 2.5,
            },
            {
                "name": "Crunches",
                "description": "Crunch upper body toward knees to work abs.",
                "muscle_group": "core",
                "equipment_needed": "",
                "difficulty_level": "beginner",
                "calories_burn_estimate": 90,
                "met_value": 2.8,
            },
            {
                "name": "Cable Woodchops",
                "description": "Twist body pulling cable diagonally across body.",
                "muscle_group": "core",
                "equipment_needed": "Cable Machine",
                "difficulty_level": "intermediate",
                "calories_burn_estimate": 110,
                "met_value": 3.5,
            },
            {
                "name": "Leg Raises",
                "description": "Raise legs while hanging or lying to strengthen lower abs.",
                "muscle_group": "core",
                "equipment_needed": "Pull-up Bar",
                "difficulty_level": "intermediate",
                "calories_burn_estimate": 120,
                "met_value": 3.8,
            },
            {
                "name": "Russian Twists",
                "description": "Twist torso side to side with weight to work obliques.",
                "muscle_group": "core",
                "equipment_needed": "Weight Plate",
                "difficulty_level": "beginner",
                "calories_burn_estimate": 100,
                "met_value": 3.0,
            },
            # FULL BODY
            {
                "name": "Burpees",
                "description": "Full body exercise combining squat, push-up, and jump.",
                "muscle_group": "full_body",
                "equipment_needed": "",
                "difficulty_level": "advanced",
                "calories_burn_estimate": 200,
                "met_value": 7.0,
            },
            {
                "name": "Mountain Climbers",
                "description": "Dynamic core exercise that works full body.",
                "muscle_group": "full_body",
                "equipment_needed": "",
                "difficulty_level": "intermediate",
                "calories_burn_estimate": 160,
                "met_value": 5.5,
            },
            {
                "name": "Kettlebell Swings",
                "description": "Swing kettlebell explosively to work full body.",
                "muscle_group": "full_body",
                "equipment_needed": "Kettlebell",
                "difficulty_level": "intermediate",
                "calories_burn_estimate": 180,
                "met_value": 6.0,
            },
            {
                "name": "Rowing Machine",
                "description": "Pull and push with legs and arms on rowing machine.",
                "muscle_group": "full_body",
                "equipment_needed": "Rowing Machine",
                "difficulty_level": "intermediate",
                "calories_burn_estimate": 170,
                "met_value": 5.8,
            },
            {
                "name": "Jump Rope",
                "description": "Classic cardio exercise that engages full body.",
                "muscle_group": "full_body",
                "equipment_needed": "Jump Rope",
                "difficulty_level": "beginner",
                "calories_burn_estimate": 150,
                "met_value": 5.0,
            },
        ]

        created_count = 0
        for data in exercises_data:
            # Deduplicate: if multiple rows share the same name, keep the first
            duplicates = Exercise.objects.filter(name=data["name"])
            if duplicates.count() > 1:
                keep = duplicates.first()
                duplicates.exclude(pk=keep.pk).delete()
                self.stdout.write(self.style.WARNING(
                    f'⚠ Removed duplicate entries for "{data["name"]}"'
                ))

            exercise, created = Exercise.objects.update_or_create(
                name=data["name"],
                defaults={
                    "description": data["description"],
                    "muscle_group": data["muscle_group"],
                    "equipment_needed": data["equipment_needed"],
                    "difficulty_level": data["difficulty_level"],
                    "calories_burn_estimate": data["calories_burn_estimate"],
                    "met_value": data["met_value"],
                },
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created exercise: "{exercise.name}"')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'⊘ Exercise already exists: "{exercise.name}"'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(f"\n✓ Seeded {created_count} new exercises successfully!")
        )
