from flask import Flask, send_from_directory
from flask_cors import CORS

from backend.api.routes import api
from backend.config import APP_TITLE, BASE_DIR


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "frontend" / "templates"),
        static_folder=str(BASE_DIR / "frontend" / "static"),
    )

    # The frontend is served by Flask, while all dashboard data comes
    # through REST endpoints under /api.
    CORS(app)

    app.config["JSON_SORT_KEYS"] = False
    app.register_blueprint(api)

    @app.get("/")
    def dashboard():
        return send_from_directory(
            BASE_DIR / "frontend" / "templates",
            "index.html",
        )

    @app.get("/favicon.ico")
    def favicon():
        return ("", 204)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
