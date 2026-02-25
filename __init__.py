from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.diagnosis import bp as diagnosis_bp
    app.register_blueprint(diagnosis_bp)

    from app.routes.appointments import bp as appointments_bp
    app.register_blueprint(appointments_bp)

    from app.routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    return app
