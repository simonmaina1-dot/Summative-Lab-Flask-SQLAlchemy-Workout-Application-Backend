import os
import sys
sys.path.insert(0, os.path.dirname(__file__) + '/..')
from marshmallow import fields, Schema, validate
from server.models import Exercise, Workout, WorkoutExercise

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(validate=validate.Range(min=0), load_default=0)
    sets = fields.Int(validate=validate.Range(min=1), load_default=1)
    duration_seconds = fields.Int(validate=validate.Range(min=0), load_default=0)

    # Nested for stretch
    exercise = fields.Nested('ExerciseSchema', dump_only=True)
    workout = fields.Nested('WorkoutSchema', dump_only=True)

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2, max=50))
    category = fields.Str(required=True, validate=validate.OneOf(['strength', 'cardio', 'flexibility', 'balance']))
    equipment_needed = fields.Bool(load_default=False)

    # Schema validations (2+): length and oneof

    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str()

    # Schema validations: range on duration

    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)

# Plain for POST add
workout_exercise_add_schema = WorkoutExerciseSchema(only=['reps', 'sets', 'duration_seconds'], exclude=('id', 'workout_id', 'exercise_id'))
