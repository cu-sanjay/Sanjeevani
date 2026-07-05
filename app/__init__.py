import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SESSION_SECRET", "sanjeevani-dev-key")

    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    instance_dir = os.path.join(base_dir, "instance")
    os.makedirs(instance_dir, exist_ok=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        instance_dir, "sanjeevani.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes.main_routes import main_bp
    from app.routes.symptom_routes import symptom_bp
    from app.routes.medicine_routes import medicine_bp
    from app.routes.resource_routes import resource_bp
    from app.routes.nutrition_routes import nutrition_bp
    from app.routes.reminder_routes import reminder_bp
    from app.routes.assistant_routes import assistant_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(symptom_bp, url_prefix="/symptom-checker")
    app.register_blueprint(medicine_bp, url_prefix="/medicines")
    app.register_blueprint(resource_bp, url_prefix="/find-care")
    app.register_blueprint(nutrition_bp, url_prefix="/nutrition")
    app.register_blueprint(reminder_bp, url_prefix="/reminders")
    app.register_blueprint(assistant_bp, url_prefix="/assistant")

    with app.app_context():
        from app import models

        db.create_all()

    @app.context_processor
    def inject_globals():
        return {"app_name": "Sanjeevani"}

    @app.errorhandler(404)
    def not_found(error):
        from flask import render_template

        return render_template("404.html"), 404

    return app
