from flask import Flask
from .config import Config
from .extensions import db, migrate,init_firebase
from app.auth.routes import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    from app import models

    init_firebase()
    
    app.register_blueprint(auth_bp)
    
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
