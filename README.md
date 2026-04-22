# Flask SQLAlchemy Workout Application Backend

## Project Description
A RESTful API backend for managing workouts, exercises, and workout-exercise associations using Flask, SQLAlchemy, and Marshmallow. Supports CRUD operations with full validation, constraints, relationships, and serialization.

Key features:
- Models: Exercise, Workout, WorkoutExercise (many-to-many through table)
- Multiple model/table/schema validations and constraints
- Nested serialization

## Installation Instructions
1. Ensure Python 3.12+ and pipenv installed.
2. ```bash
   pipenv install
   ```
3. Initialize/migrate database:
   ```bash
   pipenv run flask db init  # First time only
   pipenv run flask db migrate
   pipenv run flask db upgrade
   ```
4. Seed example data:
   ```bash
   pipenv run python seed.py
   ```

## Run Instructions
```bash
pipenv run flask run --port=5555 --debug
```
Database stored at `instance/app.db`. App runs at http://localhost:5555

## API Endpoints

### Workouts
- `GET /workouts` - List all workouts
- `GET /workouts/<int:id>` - Show workout with nested exercises
- `POST /workouts` - Create workout (body: {"date":"2024-10-01", "duration_minutes":45, "notes":"..."})
- `DELETE /workouts/<int:id>` - Delete workout (cascade deletes associations)

### Exercises
- `GET /exercises` - List all exercises
- `GET /exercises/<int:id>` - Show exercise
- `POST /exercises` - Create exercise (body: {"name":"Pushups", "category":"strength", "equipment_needed":false})
- `DELETE /exercises/<int:id>` - Delete exercise

### WorkoutExercises (Associations)
- `POST /workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises` - Add exercise to workout (body: {"sets":3, "reps":15, "duration_seconds":0})

**Validation Errors**: Return 422 with messages.
**Not Found**: 404 JSON error.

## Dependencies
See [Pipfile](Pipfile).

## Testing
- Run seed.py for data.
- Use curl/Postman for endpoints.
- Validations/constraints enforced (e.g., duration >0, category enum).

Repo ready for submission!
