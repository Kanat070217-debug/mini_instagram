# routes/posts.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from models import db, Post, User, Like

posts_bp = Blueprint("posts", __name__)



def error_response(code: str, message: str, http_status: int):
    return jsonify({
        "error": {
            "code": code,
            "message": message
        }
    }), http_status


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


@posts_bp.route("", methods=["GET"])
def list_posts():
    posts = Post.query.order_by(Post.created_at.desc(), Post.id.desc()).all()

    viewer_id = None
    try:
        verify_jwt_in_request(optional=True)
        viewer_id = int(get_jwt_identity())
    except Exception:
        viewer_id = None

    items = []
    for p in posts:
        author = User.query.get(p.author_id)
        likes_count = Like.query.filter_by(post_id=p.id).count()
        liked_by_me = False
        if viewer_id is not None:
            liked_by_me = Like.query.filter_by(
                post_id=p.id, user_id=viewer_id
            ).first() is not None

        items.append({
            "id": p.id,
            "caption": p.caption,
            "created_at": p.created_at.isoformat() + "Z",
            "author": {
                "id": author.id,
                "username": author.username,
                "avatar_url": None
            },
            "media": [],
            "stats": {
                "likes_count": likes_count,
                "comments_count": 0
            },
            "viewer": (
                {"liked_by_me": liked_by_me}
                if viewer_id is not None else {}
            )
        })

    return jsonify({
        "items": items,
        "paging": {
            "limit": len(items),
            "offset": 0,
            "next_offset": None
        }
    }), 200
