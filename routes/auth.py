# routes/auth.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import db, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def error_response(code: str, message: str, http_status: int, details=None):
    body = {
        "error": {
            "code": code,
            "message": message
        }
    }
    if details is not None:
        body["error"]["details"] = details
    return jsonify(body), http_status


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return error_response(
            "BAD_REQUEST",
            "username, email, password required",
            400
        )

    if User.query.filter_by(username=username).first():
        return error_response(
            "RESOURCE_CONFLICT",
            "Username already exists",
            409,
            {"field": "username"}
        )

    if User.query.filter_by(email=email).first():
        return error_response(
            "RESOURCE_CONFLICT",
            "Email already exists",
            409,
            {"field": "email"}
        )

    user = User(
        username=username,
        email=email,
        password=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return error_response(
            "BAD_REQUEST",
            "username and password required",
            400
        )

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return error_response(
            "UNAUTHORIZED",
            "Invalid username or password",
            401
        )

    access_token = create_access_token(identity=str(user.id))



    return jsonify({
        "access_token": access_token,
        "token_type": "Bearer"
    }), 200
