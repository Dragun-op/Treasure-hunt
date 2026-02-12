from flask import Blueprint, render_template, g, current_app, session,request, session, abort
from app.utils.decorators import firebase_required
from firebase_admin import auth as firebase_auth
from app.extensions import db
from app.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/test")
def auth_test():
    return render_template(
        "auth/landing.html",
        firebase_config={
            "apiKey": current_app.config["FIREBASE_API_KEY"],
            "authDomain": current_app.config["FIREBASE_AUTH_DOMAIN"],
            "projectId": current_app.config["FIREBASE_PROJECT_ID"],
        }
    )


@auth_bp.route("/me")
@firebase_required
def me():
    user = g.current_user
    return {
        "id": user.id,
        "firebase_uid": user.firebase_uid,
        "email": user.email,
        "team_id": user.team_id,
        "role": user.role,
    }

@auth_bp.route("/session", methods=["POST"])
def create_session():
    id_token = request.headers.get("Authorization")

    if not id_token:
        abort(401, "Missing token")

    try:
        decoded = firebase_auth.verify_id_token(id_token.split("Bearer ")[-1])
    except Exception:
        abort(401, "Invalid Firebase token")

    firebase_uid = decoded["uid"]
    email = decoded.get("email")

    # ---- CRITICAL PART ----
    user = User.query.filter_by(firebase_uid=firebase_uid).first()

    if not user:
        user = User(
            firebase_uid=firebase_uid,
            email=email,
            role="member"
        )
        db.session.add(user)
        db.session.commit()

    session["firebase_uid"] = firebase_uid

    return {"message": "Session created"}
