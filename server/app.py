import os
import sys
sys.path.insert(0, os.path.dirname(__file__) + '/..')
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow.exceptions import ValidationError
from models import db, Exercise, Workout, WorkoutExercise
from server.schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema, workout_exercise_add_schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Helper functions
def get_workout_or_404(workout_id):
    workout = Workout.query.get_or_404(workout_id)
    return workout

def get_exercise_or_404(exercise_id):
    exercise = Exercise.query.get_or_404(exercise_id)
    return exercise

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

# Workouts endpoints
@app.route('/workouts', methods=['GET'])
def index_workouts():
    workouts = Workout.query.all()
    return jsonify(WorkoutSchema(many=True).dump(workouts))

@app.route('/workouts/<int:id>', methods=['GET'])
def show_workout(id):
    workout = get_workout_or_404(id)
    return jsonify(WorkoutSchema().dump(workout))

@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = request.get_json()
        schema = WorkoutSchema()
        workout = schema.load(data)
        db.session.add(workout)
        db.session.commit()
        return jsonify(schema.dump(workout)), 201
    except ValidationError as err:
        return jsonify(err.messages), 422

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = get_workout_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return '', 204

# Exercises endpoints
@app.route('/exercises', methods=['GET'])
def index_exercises():
    exercises = Exercise.query.all()
    return jsonify(ExerciseSchema(many=True).dump(exercises))

@app.route('/exercises/<int:id>', methods=['GET'])
def show_exercise(id):
    exercise = get_exercise_or_404(id)
    return jsonify(ExerciseSchema().dump(exercise))

@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = request.get_json()
        schema = ExerciseSchema()
        exercise = schema.load(data)
        db.session.add(exercise)
        db.session.commit()
        return jsonify(schema.dump(exercise)), 201
    except ValidationError as err:
        return jsonify(err.messages), 422

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = get_exercise_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return '', 204

# Add exercise to workout
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def create_workout_exercise(workout_id, exercise_id):
    get_workout_or_404(workout_id)
    get_exercise_or_404(exercise_id)
    try:
        data = request.get_json() or {}
        validated_data = dict(workout_exercise_add_schema.load(data) or {})
        we = WorkoutExercise()
        we.workout_id = workout_id
        we.exercise_id = exercise_id
        we.reps = validated_data.get('reps', 0)
        if 'sets' in validated_data:
            we.sets = validated_data['sets']
        we.duration_seconds = validated_data.get('duration_seconds', 0)
        db.session.add(we)
        db.session.commit()
        return jsonify(WorkoutExerciseSchema().dump(we)), 201
    except ValidationError as err:
        return jsonify(err.messages), 422

if __name__ == '__main__':
    app.run(port=5555, debug=True)
