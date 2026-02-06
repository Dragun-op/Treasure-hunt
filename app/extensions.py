import os
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(
            os.getenv("FIREBASE_CREDENTIALS")
        )
        firebase_admin.initialize_app(cred)


db = SQLAlchemy()
migrate = Migrate()
