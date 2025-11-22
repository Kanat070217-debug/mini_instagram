from flask import Flask, jsonify
from config import Config
from models import db
from routes.auth import auth_bp
from routes.posts import posts_bp
from routes.likes import likes_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(posts_bp, url_prefix="/posts")
    app.register_blueprint(likes_bp, url_prefix="/likes")

    # Health check endpoint
    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    with app.app_context():
        db.create_all()

    return app


# Gunicorn көретін негізгі app
app = create_app()
