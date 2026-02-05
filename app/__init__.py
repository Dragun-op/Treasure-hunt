from flask import Flask
from .config import Config
from .extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models

    #test db connection
    # with app.app_context():
    #     try:
    #         db.engine.connect()
    #         print(" Database connected")
    #     except Exception as e:
    #         print(" Database connection failed:", e)


    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app
