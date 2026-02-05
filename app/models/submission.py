from datetime import datetime
from app.extensions import db

class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)

    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey("levels.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    submitted_answer = db.Column(db.Text)
    is_correct = db.Column(db.Boolean)

    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
