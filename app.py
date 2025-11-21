# app.py
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from models import db
from config import Config

from routes.auth import auth_bp
from routes.posts import posts_bp
from routes.likes import likes_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)

    # маршруттар
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(likes_bp)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "error": {
                "code": "NOT_FOUND",
                "message": "Resource not found"
            }
        }), 404

    return app


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
