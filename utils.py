from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from config import Config
from extensions import db, jwt, migrate
from books.routes import books_bp
from users.routes import users_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=config_class.ALLOWED_CORS_ORIGINS)

    app.register_blueprint(books_bp)
    app.register_blueprint(users_bp)

    return app


def register_swagger(app: Flask, docs_file: str) -> Flask:
    """
    Register Swagger with JWT authorization support
    """

    app.config["SWAGGER"] = {
        "title": "Online Library System API",
        "uiversion": 3,
        "termsOfService": None,
        "favicon": "https://rdi-eg.ai/wp-content/uploads/2020/10/cropped-icon-32x32.png",
    }

    swagger_config = Swagger.DEFAULT_CONFIG
    swagger_config.update(
        {
            "swagger_ui_bundle_js": "//cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.52.4/swagger-ui-bundle.min.js",
            "swagger_ui_standalone_preset_js": "//cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.52.4/swagger-ui-standalone-preset.min.js",
            "jquery_js": "//unpkg.com/jquery@2.2.4/dist/jquery.min.js",
            "swagger_ui_css": "//cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.52.4/swagger-ui.min.css",
            "headers": [
                ("Access-Control-Allow-Origin", "*"),
                ("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"),
                ("Access-Control-Allow-Headers", "Content-Type, Authorization"),
            ],
            "specs_route": "/apidocs/",
        }
    )

    Swagger(app, template_file=docs_file, config=swagger_config)

    return app
