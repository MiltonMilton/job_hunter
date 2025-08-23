import os
from typing import Any

from flask import Flask, jsonify
from flask_migrate import Migrate, upgrade

from models import User, db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "AUTH_DATABASE_URL", "mysql+pymysql://root:password@localhost/auth_db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)

    @app.route("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.route("/users")
    def list_users() -> list[dict[str, Any]]:
        users = User.query.all()
        return jsonify(
            [
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "created_at": user.created_at.isoformat(),
                }
                for user in users
            ]
        )

    return app


app = create_app()


if __name__ == "__main__":
    with app.app_context():
        upgrade()
    app.run(host="0.0.0.0", port=8000)

