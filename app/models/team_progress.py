from datetime import datetime
from app.extensions import db

class TeamProgress(db.Model):
    __tablename__ = "team_progress"

    id = db.Column(db.Integer, primary_key=True)

    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey("levels.id"), nullable=False)

    status = db.Column(db.String(20), default="locked")  
    # locked | unlocked | completed

    unlocked_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
