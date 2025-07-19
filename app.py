import os

from utils import create_app, register_swagger


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_PATH = os.path.join(BASE_DIR, "static", "docs.yml")
app = create_app()
app = register_swagger(app, DOCS_PATH)

if __name__ == "__main__":
    app.run(
        debug=int(os.getenv("FLASK_DEBUG", "1")) == 1,
        host="0.0.0.0",
        port=int(os.getenv("SERVER_PORT", "5000")),
        threaded=True,
    )
