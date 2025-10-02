from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    created_at = db.Column(db.Date, default=date.today)
    # store the last completion date (ISO string) to keep it simple
    last_completed = db.Column(db.String(10), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "last_completed": self.last_completed
        }
