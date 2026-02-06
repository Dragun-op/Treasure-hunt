import secrets
from flask import Blueprint, request, g, abort
from app.extensions import db
from app.utils.decorators import firebase_required
from app.models import Team, User

team_bp = Blueprint("team", __name__, url_prefix="/team")

@team_bp.route("/create", methods=["POST"])
@firebase_required
def create_team():
    user = g.current_user

    if user.team_id is not None:
        abort(400, "User already in a team")

    data = request.get_json()
    team_name = data.get("name")

    if not team_name:
        abort(400, "Team name required")

    invite_code = secrets.token_hex(4)

    team = Team(
        name=team_name,
        invite_code=invite_code,
        current_level=1,
    )

    db.session.add(team)
    db.session.flush()  # get team.id without commit

    user.team_id = team.id
    user.role = "leader"

    db.session.commit()

    return {
        "team_id": team.id,
        "team_name": team.name,
        "invite_code": team.invite_code,
        "role": user.role,
    }

@team_bp.route("/join", methods=["POST"])
@firebase_required
def join_team():
    user = g.current_user

    if user.team_id is not None:
        abort(400, "User already in a team")

    data = request.get_json()
    invite_code = data.get("invite_code")

    if not invite_code:
        abort(400, "Invite code required")

    team = Team.query.filter_by(invite_code=invite_code).first()

    if not team:
        abort(404, "Invalid invite code")

    if len(team.members) >= team.max_size:
        abort(403, "Team is full")

    if team.is_disqualified:
        abort(403, "Team is disqualified")

    user.team_id = team.id
    user.role = "member"

    db.session.commit()

    return {
        "team_id": team.id,
        "team_name": team.name,
        "role": user.role,
    }

@team_bp.route("/me")
@firebase_required
def my_team():
    user = g.current_user

    if not user.team:
        return {"team": None}

    return {
        "team": {
            "id": user.team.id,
            "name": user.team.name,
            "invite_code": user.team.invite_code,
            "current_level": user.team.current_level,
            "role": user.role,
        }
    }
