import os

from utils import create_app


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_PATH = os.path.join(BASE_DIR, "static", "docs.yml")
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

    app.run(
        debug=int(os.getenv("FLASK_DEBUG", "1")) == 1,
        host="0.0.0.0",
        port=app.config.get("SERVER_PORT", 8080),
        threaded=True,
    )
