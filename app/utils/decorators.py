from functools import wraps
from flask import request, g, session
from firebase_admin import auth
from app.models import User
from app.extensions import db


def firebase_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        # ---- 1 Check existing session first ----
        user_id = session.get("user_id")
        if user_id:
            user = User.query.get(user_id)
            if user:
                g.current_user = user
                return f(*args, **kwargs)

        # ---- 2️ If no session, check Authorization header ----
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return "Missing Firebase token", 401

        token = auth_header.split(" ")[1]

        try:
            decoded_token = auth.verify_id_token(token)
        except Exception:
            return "Invalid Firebase token", 401

        firebase_uid = decoded_token.get("uid")

        if not firebase_uid:
            return "Invalid Firebase token payload", 401

        user = User.query.filter_by(firebase_uid=firebase_uid).first()

        if not user:
            return "User not found", 401

        # ---- 3️ Create session ----
        session["user_id"] = user.id
        g.current_user = user

        return f(*args, **kwargs)

    return decorated
