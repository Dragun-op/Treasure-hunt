from flask import Blueprint, render_template, g, current_app
from app.utils.decorators import firebase_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/test")
def auth_test():
    return render_template(
        "landing.html",
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

