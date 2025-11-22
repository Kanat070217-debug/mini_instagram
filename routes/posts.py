# routes/posts.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from models import db, Post, User, Like

# МҰНДА ЕНДІ ЕШҚАНДАЙ url_prefix ЖОҚ!
posts_bp = Blueprint("posts", __name__)


def error_response(code: str, message: str, http_status: int):
    return jsonify({
        "error": {
            "code": code,
            "message": message
        }
    }), http_status


# Пост жасау (POST /posts)
@posts_bp.route("", methods=["POST"])
@jwt_required()
def create_post():
    data = request.get_json() or {}
    caption = data.get("caption")

    if not caption:
        return error_response(
            "BAD_REQUEST",
            "caption is required",
            400
        )

    user_id = int(get_jwt_identity())
    post = Post(caption=caption, author_id=user_id)
    db.session.add(post)
    db.session.commit()

    return jsonify({
        "id": post.id,
        "created_at": post.created_at.isoformat() + "Z"
    }), 201


# Барлық посттарды көру (GET /posts)
@posts_bp.route("", methods=["GET"])
def list_posts():
    # Қарапайым вариант: бар посттардың бәрін қайтару
    posts = Post.query.order_by(Post.created_at.desc()).all()

    items = []
    for p in posts:
        items.append({
            "id": p.id,
            "caption": p.caption,
            "author": {
                "id": p.author.id,
                "username": p.author.username,
                "avatar_url": p.author.avatar_url if hasattr(p.author, "avatar_url") else None
            },
            "created_at": p.created_at.isoformat() + "Z",
            "media": [],
            "stats": {
                "likes_count": 0,
                "comments_count": 0
            },
            "viewer": {}
        })

    return jsonify({
        "items": items,
        "paging": {
            "offset": 0,
            "limit": len(items),
            "next_offset": None
        }
    })
