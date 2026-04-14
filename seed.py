#!/usr/bin/env python3

import sys
from datetime import date

# Add root to path for imports
sys.path.insert(0, '.')

from server.app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    # Reset database
    db.drop_all()
    db.create_all()

    # Seed Exercises
    exercises_data = [
        {'name': 'Pushups', 'category': 'strength', 'equipment_needed': False},
        {'name': 'Squats', 'category': 'strength', 'equipment_needed': False},
        {'name': 'Running', 'category': 'cardio', 'equipment_needed': True},
        {'name': 'Plank', 'category': 'strength', 'equipment_needed': False},
    ]
    exercises = [Exercise(**data) for data in exercises_data]
    db.session.bulk_save_objects(exercises)
    db.session.commit()

    # Seed Workouts
    workouts_data = [
        {'date': date(2024, 10, 1), 'duration_minutes': 45, 'notes': 'Full body strength'},
        {'date': date(2024, 10, 2), 'duration_minutes': 30, 'notes': 'Cardio focus'},
    ]
    workouts = [Workout(**data) for data in workouts_data]
    db.session.bulk_save_objects(workouts)
    db.session.commit()

    # Seed WorkoutExercises
    workout_exercises = [
        WorkoutExercise(workout_id=1, exercise_id=1, sets=3, reps=15),  # Workout 1 - Pushups
        WorkoutExercise(workout_id=1, exercise_id=2, sets=4, reps=12),  # Workout 1 - Squats
        WorkoutExercise(workout_id=2, exercise_id=3, sets=1, duration_seconds=1800),  # Workout 2 - Running 30min
        WorkoutExercise(workout_id=2, exercise_id=4, sets=3, reps=60),  # Workout 2 - Plank (60s per rep)
    ]
    db.session.bulk_save_objects(workout_exercises)
    db.session.commit()

    print(f"Seeded: {Exercise.query.count()} exercises, {Workout.query.count()} workouts, {WorkoutExercise.query.count()} workout_exercises")

    # Quick relationship test
    workout1 = Workout.query.first()
    print(f"Workout 1 has {len(workout1.workout_exercises)} exercises")
    if workout1.workout_exercises:
        print(f"First exercise: {workout1.workout_exercises[0].exercise.name}")
