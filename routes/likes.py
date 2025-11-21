# routes/likes.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Like, Post

likes_bp = Blueprint("likes", __name__)


def error_response(code: str, message: str, http_status: int):
    return jsonify({
        "error": {
            "code": code,
            "message": message
        }
    }), http_status


@likes_bp.route("/posts/<int:post_id>/like", methods=["POST"])
@jwt_required()
def like_post(post_id):
    user_id = int(get_jwt_identity())

    post = Post.query.get(post_id)
    if not post:
        return error_response("NOT_FOUND", "Post not found", 404)

    existing = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
    if existing:
        likes_count = Like.query.filter_by(post_id=post_id).count()
        return jsonify({
            "liked": True,
            "likes_count": likes_count
        }), 200

    like = Like(user_id=user_id, post_id=post_id)
    db.session.add(like)
    db.session.commit()

    likes_count = Like.query.filter_by(post_id=post_id).count()
    return jsonify({
        "liked": True,
        "likes_count": likes_count
    }), 200


@likes_bp.route("/posts/<int:post_id>/like", methods=["DELETE"])
@jwt_required()
def unlike_post(post_id):
    user_id = int(get_jwt_identity())

    post = Post.query.get(post_id)
    if not post:
        return error_response("NOT_FOUND", "Post not found", 404)

    existing = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()

    likes_count = Like.query.filter_by(post_id=post_id).count()
    return jsonify({
        "liked": False,
        "likes_count": likes_count
    }), 200
