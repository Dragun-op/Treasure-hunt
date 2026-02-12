from flask import Blueprint, g, redirect, url_for, abort,render_template
from app.utils.decorators import firebase_required
from flask import request, jsonify
from app.extensions import db
from app.utils.crypto import hash_answer
from app.models import Submission, TeamProgress, Level
from datetime import datetime
from app.level.level1 import validate_environment


game_bp = Blueprint("game", __name__, url_prefix="/game")

@game_bp.route("/start")
@firebase_required
def game_start():
    user = g.current_user

    if not user.team:
        return redirect(url_for("auth.auth_test"))  # later: team page

    # Find highest unlocked or active level
    progress = (
        TeamProgress.query
        .filter_by(team_id=user.team.id)
        .order_by(TeamProgress.level_id.desc())
        .first()
    )

    if not progress:
        abort(500, "Team progress not initialized")

    level = Level.query.get(progress.level_id)

    return render_template("game/start.html",
                    user=user,
                    team=user.team,
                    level=level)

@game_bp.route("/level/<int:level_number>")
@firebase_required
def level(level_number):
    user = g.current_user

    if not user.team:
        abort(403)

    level = Level.query.filter_by(level_number=level_number).first_or_404()

    progress = TeamProgress.query.filter_by(
        team_id=user.team.id,
        level_id=level.id
    ).first()

    if not progress or progress.status == "locked":
        abort(403)

    template_name = f"game/level_{level_number}.html"

    try:
        return render_template(template_name,
                                user=user,
                                team=user.team, 
                                level=level)
    except:
        return render_template("game/level_generic.html", 
                               user=user, 
                               team=user.team, 
                               level=level)

@game_bp.route("/level/<int:level_number>/submit", methods=["POST"])
@firebase_required
def submit_answer(level_number):
    user = g.current_user

    if not user.team:
        abort(403, "User not in team")

    level = Level.query.filter_by(level_number=level_number).first_or_404()

    progress = TeamProgress.query.filter_by(
        team_id=user.team.id,
        level_id=level.id
    ).first()

    if not progress or progress.status != "unlocked":
        abort(403, "Level not unlocked")

    data = request.get_json()
    submitted_answer = data.get("answer")

    if not submitted_answer:
        abort(400, "Answer required")

    submitted_hash = hash_answer(submitted_answer)
    is_correct = submitted_hash in level.answer_hashes

    try:
        # ---- TRANSACTION START ----

        submission = Submission(
            team_id=user.team.id,
            level_id=level.id,
            user_id=user.id,
            submitted_answer=submitted_answer,
            is_correct=is_correct
        )
        db.session.add(submission)

        if is_correct:
            # mark current level completed
            progress.status = "completed"
            progress.completed_at = datetime.utcnow()

            # unlock next level if exists
            next_level = Level.query.filter_by(
                level_number=level_number + 1,
                is_active=True
            ).first()

            if next_level:
                existing_next = TeamProgress.query.filter_by(
                    team_id=user.team.id,
                    level_id=next_level.id
                ).first()

                if not existing_next:
                    new_progress = TeamProgress(
                        team_id=user.team.id,
                        level_id=next_level.id,
                        status="unlocked",
                        unlocked_at=datetime.utcnow()
                    )
                    db.session.add(new_progress)

                user.team.current_level = next_level.level_number

        db.session.commit()
        # ---- TRANSACTION END ----

    except Exception:
        db.session.rollback()
        abort(500, "Submission failed")

    return jsonify({
        "correct": is_correct,
        "next_level_unlocked": is_correct
    })

@game_bp.route("/level/1/environment", methods=["POST"])
@firebase_required
def level1_environment():
    is_valid, message = validate_environment()

    if not is_valid:
        return jsonify({"success": False, "message": message})

    return jsonify({
        "success": True,
        "password": message
    })
