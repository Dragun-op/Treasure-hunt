from datetime import datetime
from app.extensions import db

class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    invite_code = db.Column(db.String(20), unique=True, index=True, nullable=False)

    max_size = db.Column(db.Integer, default=4)
    current_level = db.Column(db.Integer, default=1)

    is_disqualified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    members = db.relationship("User", backref="team", lazy=True)
