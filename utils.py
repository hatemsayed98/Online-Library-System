from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, jwt, migrate 


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=config_class.ALLOWED_CORS_ORIGINS)


    return app

