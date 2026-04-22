#!/usr/bin/env python3

import sys
from datetime import date

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
    we1 = WorkoutExercise()
    we1.workout_id = 1
    we1.exercise_id = 1
    we1.sets = 3
    we1.reps = 15  # Workout 1 - Pushups
    
    we2 = WorkoutExercise()
    we2.workout_id = 1
    we2.exercise_id = 2
    we2.sets = 4
    we2.reps = 12  # Workout 1 - Squats
    
    we3 = WorkoutExercise()
    we3.workout_id = 2
    we3.exercise_id = 3
    we3.sets = 1
    we3.duration_seconds = 1800  # Workout 2 - Running 30min
    
    we4 = WorkoutExercise()
    we4.workout_id = 2
    we4.exercise_id = 4
    we4.sets = 3
    we4.reps = 60  # Workout 2 - Plank (60s per rep)
    
    workout_exercises = [we1, we2, we3, we4]
    db.session.bulk_save_objects(workout_exercises)
    db.session.commit()

    print(f"Seeded: {Exercise.query.count()} exercises, {Workout.query.count()} workouts, {WorkoutExercise.query.count()} workout_exercises")

    # Quick relationship test
    workout1 = Workout.query.first()
    if workout1:
        print(f"Workout 1 has {len(workout1.workout_exercises)} exercises")
        if workout1.workout_exercises:
            print(f"First exercise: {workout1.workout_exercises[0].exercise.name}")
