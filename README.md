# Habit Tracker

Simple full-stack habit tracker built with:
- Python (Flask) backend
- SQLite + SQLAlchemy
- HTML, CSS, vanilla JavaScript frontend

## Run locally
1. Create venv: `python -m venv venv` and activate
2. `pip install -r requirements.txt`
3. `python db_init.py`
4. `python app.py`
5. Open http://127.0.0.1:5000/

## API
- `GET /api/habits` - list
- `POST /api/habits` - add {name}
- `POST /api/habits/<id>/toggle` - toggle today's completion
- `DELETE /api/habits/<id>` - delete

## Goals & roadmap
- Add user auth
- Track streaks & history
- Deploy (Heroku / Render / Docker)
