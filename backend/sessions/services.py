def calculate_calories(session):
    total = 0
    user_weight = float(session.user.weight_kg or 0)
    for log in session.logs.filter(completed=True):
        duration_hours = log.duration_seconds / 3600
        met = float(log.exercise.met_value)
        total += met * user_weight * duration_hours
    session.calories_burned = round(total, 2)
    session.save(update_fields=["calories_burned"])
