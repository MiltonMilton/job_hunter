import os

from flask import Flask
from flask_migrate import Migrate, upgrade

from models import db, User


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

    return app


app = create_app()


if __name__ == "__main__":
    with app.app_context():
        upgrade()
    app.run(host="0.0.0.0", port=8000)

