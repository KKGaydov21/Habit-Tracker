from flask import Flask, jsonify, request, render_template
from models import db, Habit
from datetime import date

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habit.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    # API: list habits
    @app.route('/api/habits', methods=['GET'])
    def list_habits():
        habits = Habit.query.order_by(Habit.id).all()
        return jsonify([h.to_dict() for h in habits])

    # API: add habit
    @app.route('/api/habits', methods=['POST'])
    def add_habit():
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        if not name:
            return jsonify({"error": "Missing name"}), 400
        habit = Habit(name=name)
        db.session.add(habit)
        db.session.commit()
        return jsonify(habit.to_dict()), 201

    # API: toggle completion for today
    @app.route('/api/habits/<int:habit_id>/toggle', methods=['POST'])
    def toggle_habit(habit_id):
        habit = Habit.query.get_or_404(habit_id)
        today_iso = date.today().isoformat()
        if habit.last_completed == today_iso:
            habit.last_completed = None
        else:
            habit.last_completed = today_iso
        db.session.commit()
        return jsonify(habit.to_dict())

    # API: delete habit
    @app.route('/api/habits/<int:habit_id>', methods=['DELETE'])
    def delete_habit(habit_id):
        habit = Habit.query.get_or_404(habit_id)
        db.session.delete(habit)
        db.session.commit()
        return jsonify({"success": True})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
