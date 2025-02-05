from flask import Flask
from app.routes import main_bp

# App version
VERSION = "BETA V0.3.0"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "your_secret_key_here"

    app.register_blueprint(main_bp)

    @app.context_processor
    def inject_version():
        return {"version": VERSION}

    return app
