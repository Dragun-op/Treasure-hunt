from functools import wraps
from flask import request, g, abort
from firebase_admin import auth as firebase_auth
from app.models import User
from app.extensions import db

def firebase_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            abort(401, "Missing Firebase token")

        token = auth_header.split(" ")[1]

        try:
            decoded = firebase_auth.verify_id_token(token)
        except Exception:
            abort(401, "Invalid Firebase token")

        firebase_uid = decoded["uid"]
        email = decoded.get("email")
        name = decoded.get("name")

        # AUTO-CREATE USER
        user = User.query.filter_by(firebase_uid=firebase_uid).first()

        if not user:
            user = User(
                firebase_uid=firebase_uid,
                email=email,
                name=name,
            )
            db.session.add(user)
            db.session.commit()

        g.current_user = user
        g.firebase_claims = decoded

        return fn(*args, **kwargs)

    return wrapper
