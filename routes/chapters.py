from flask import Blueprint, jsonify
from models import Chapter

chapters_bp = Blueprint("chapters", __name__)


@chapters_bp.route("/chapters")
def list_chapters():
    chapters = Chapter.query.filter_by(is_published=True).order_by(Chapter.order).all()
    return jsonify([c.to_dict() for c in chapters])


@chapters_bp.route("/chapters/<slug>")
def get_chapter(slug):
    chapter = Chapter.query.filter_by(slug=slug, is_published=True).first()
    if not chapter:
        return jsonify({"error": "Chapter not found"}), 404
    return jsonify(chapter.to_dict(full=True))
