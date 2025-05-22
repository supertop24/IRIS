import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app(config_class='config.DevelopmentConfig'):  # Default to DevelopmentConfig
    app = Flask(__name__)
    app.secret_key = 'keykeykey'

    app.config.from_object(config_class)  # Load the configuration
    db.init_app(app)  # Initialize SQLAlchemy
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.teacherLogin'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    with app.app_context():
        db.create_all()

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app

