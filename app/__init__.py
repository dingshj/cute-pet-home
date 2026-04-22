import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    db_uri = app.config["SQLALCHEMY_DATABASE_URI"]
    if db_uri.startswith("sqlite:///"):
        db_file = db_uri[len("sqlite:///") :]
        os.makedirs(os.path.dirname(db_file) or ".", exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.main import bp as main_bp
    from app.routes.auth import bp as auth_bp
    from app.routes.pets import bp as pets_bp
    from app.routes.services import bp as services_bp
    from app.routes.api import bp as api_bp
    from app.routes.recognize import bp as recognize_bp
    from app.routes.adoption import bp as adoption_bp
    from app.routes.shop import bp as shop_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(pets_bp, url_prefix="/pets")
    app.register_blueprint(services_bp, url_prefix="/services")
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(recognize_bp, url_prefix="/recognize")
    app.register_blueprint(adoption_bp, url_prefix="/adoption")
    app.register_blueprint(shop_bp)

    with app.app_context():
        db.create_all()
        if User.query.filter_by(username="admin").first() is None:
            u = User(username="admin", role="admin")
            u.set_password("admin123")
            db.session.add(u)
            db.session.commit()

    return app
