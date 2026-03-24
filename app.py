import os
import traceback
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

    # Auto-create tables + auto-seed on startup
    with app.app_context():
        import models  # noqa: F401
        print("Creating tables...")
        db.create_all()
        print("Tables created.")
        try:
            count = models.Chapter.query.count()
            print(f"Existing chapters: {count}")
            if count == 0:
                print("No chapters found, auto-seeding...")
                from seed.chapter0 import seed as seed_ch0
                from seed.chapter1 import seed as seed_ch1
                seed_ch0(db, models)
                seed_ch1(db, models)
                print(f"Auto-seeded {models.Chapter.query.count()} chapters")
        except Exception as e:
            print(f"Startup error: {e}")
            traceback.print_exc()

    # Health check
    @app.route("/api/health")
    def health():
        return {"status": "ok", "app": "code-chronicle"}

    # One-time seed endpoint (safe to call multiple times)
    @app.route("/api/seed")
    def seed():
        import models as M
        if M.Chapter.query.first():
            return {"status": "already seeded", "chapters": M.Chapter.query.count()}
        from seed.chapter0 import seed as seed_ch0
        from seed.chapter1 import seed as seed_ch1
        seed_ch0(db, M)
        seed_ch1(db, M)
        return {"status": "seeded", "chapters": M.Chapter.query.count()}

    return app
