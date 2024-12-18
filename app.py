import os
from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from resources.record import blp as RecordBlueprint
from flask_migrate import Migrate
from db import db
from dotenv import load_dotenv
import models


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()
    CORS(app)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    if os.getenv("FLASK_ENV") == "development":
        # Use SQLite in development
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    else:
        # Use PostgreSQL in production (e.g., Docker)
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)

    api = Api(app)
    api.register_blueprint(RecordBlueprint)

    return app
