from app.extensions import db

class Level(db.Model):
    __tablename__ = "levels"

    id = db.Column(db.Integer, primary_key=True)
    level_number = db.Column(db.Integer, unique=True, nullable=False)

    title = db.Column(db.String(200))
    description = db.Column(db.Text)

    unlock_type = db.Column(db.String(50))  # time | answer | date | system_clock
    unlock_value = db.Column(db.JSON)

    answer_hashes = db.Column(db.JSON, nullable=False, default=list)
    is_active = db.Column(db.Boolean, default=True)
