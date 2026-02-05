from datetime import datetime
from app.extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    firebase_uid = db.Column(db.String(128), unique=True, index=True, nullable=False)

    name = db.Column(db.String(120))
    email = db.Column(db.String(120))

    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=True)
    role = db.Column(db.String(20), default="member")  # leader | member

    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
