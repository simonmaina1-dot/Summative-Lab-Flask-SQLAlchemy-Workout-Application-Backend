from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint, ForeignKeyConstraint
db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    category = db.Column(db.String(30), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    # Table constraints (2+)
    # unique name, length implicit

    __table_args__ = (
        CheckConstraint('length(name) >= 2', name='check_name_length'),
    )

    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise')
    # Through relationship (read-only)
    workouts = db.relationship('Workout', secondary='workout_exercise', back_populates='exercises', viewonly=True)

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 2:
            raise AssertionError('Name must be at least 2 characters long')
        return name

    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['strength', 'cardio', 'flexibility', 'balance']
        if category.lower() not in valid_categories:
            raise AssertionError(f'Category must be one of {valid_categories}')
        return category

    def __repr__(self):
        return f'<Exercise {self.id}: {self.name}>'


class Workout(db.Model):
    __tablename__ = 'workout'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # Table constraints
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
    )

    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    # Through (read-only)
    exercises = db.relationship('Exercise', secondary='workout_exercise', back_populates='workouts', viewonly=True)

    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if duration <= 0:
            raise AssertionError('Duration must be positive')
        return duration

    @validates('date')
    def validate_date(self, key, date):
        from datetime import date as datedate
        # Allow past dates for workout tracking
        return date

    def __repr__(self):
        return f'<Workout {self.id}: {self.date}>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercise'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    reps = db.Column(db.Integer, default=0)
    sets = db.Column(db.Integer, nullable=False, default=1)
    duration_seconds = db.Column(db.Integer, default=0)

    # Table constraints
    __table_args__ = (
        CheckConstraint('sets >= 1', name='check_sets_min'),
        CheckConstraint('(reps >= 0 OR duration_seconds >= 0)', name='check_reps_or_duration'),
    )

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('sets')
    def validate_sets(self, key, sets):
        if sets < 1:
            raise AssertionError('Sets must be at least 1')
        return sets

    @validates('reps', 'duration_seconds')
    def validate_reps_or_duration(self, key, value):
        if key == 'reps' and value < 0:
            raise AssertionError('Reps cannot be negative')
        if key == 'duration_seconds' and value < 0:
            raise AssertionError('Duration cannot be negative')
        return value

    def __repr__(self):
        return f'<WorkoutExercise {self.id}: Workout{self.workout_id}-Exercise{self.exercise_id}>'
