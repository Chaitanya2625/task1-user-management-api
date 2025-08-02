from flask import Flask
from .database import db
from .routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)

    app.register_blueprint(user_bp)

    @app.route("/")
    def health():
        return {"status": "ok"}

    return app
