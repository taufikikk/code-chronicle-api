from flask import Blueprint, jsonify, request
from app import db
from models import UserProgress

progress_bp = Blueprint("progress", __name__)


@progress_bp.route("/progress/<user_id>")
def get_progress(user_id):
    """Get all chapter progress for a user."""
    progress = UserProgress.query.filter_by(user_id=user_id).all()
    return jsonify([p.to_dict() for p in progress])


@progress_bp.route("/progress/<user_id>/<int:chapter_id>", methods=["POST"])
def save_progress(user_id, chapter_id):
    """Save or update progress for a chapter."""
    data = request.get_json()

    progress = UserProgress.query.filter_by(
        user_id=user_id, chapter_id=chapter_id
    ).first()

    if not progress:
        progress = UserProgress(user_id=user_id, chapter_id=chapter_id)
        db.session.add(progress)

    if "current_scene_slug" in data:
        progress.current_scene_slug = data["current_scene_slug"]
    if "choice_made" in data:
        progress.choice_made = data["choice_made"]
    if "challenge_completed" in data:
        progress.challenge_completed = data["challenge_completed"]
    if "completed" in data:
        progress.completed = data["completed"]

    db.session.commit()
    return jsonify(progress.to_dict())
