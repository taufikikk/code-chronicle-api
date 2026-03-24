from flask import Blueprint, jsonify, request
from models import GlossaryTerm

glossary_bp = Blueprint("glossary", __name__)


@glossary_bp.route("/glossary")
def list_glossary():
    """List all glossary terms, optionally filtered up to a chapter."""
    up_to_chapter = request.args.get("up_to_chapter", type=int)

    query = GlossaryTerm.query
    if up_to_chapter:
        query = query.filter(GlossaryTerm.chapter_id <= up_to_chapter)

    terms = query.order_by(GlossaryTerm.chapter_id, GlossaryTerm.key).all()
    return jsonify([t.to_dict() for t in terms])
