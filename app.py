import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Neon PostgreSQL config — same pattern as Unstuck 日本語
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///dev.db")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "connect_args": {"sslmode": "require"} if "neon" in os.environ.get("DATABASE_URL", "") else {},
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    CORS(app, origins=os.environ.get("CORS_ORIGINS", "*").split(","))

    db.init_app(app)

    # Register routes
    from routes.chapters import chapters_bp
    from routes.glossary import glossary_bp
    from routes.progress import progress_bp

    app.register_blueprint(chapters_bp, url_prefix="/api")
    app.register_blueprint(glossary_bp, url_prefix="/api")
    app.register_blueprint(progress_bp, url_prefix="/api")

    # Health check
    @app.route("/api/health")
    def health():
        return {"status": "ok", "app": "code-chronicle"}

    return app
