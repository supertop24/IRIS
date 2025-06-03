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
    print("DB session is:", db.session)

    from .models import User, Teacher, Student
    
    with app.app_context():
        db.create_all()

        @login_manager.user_loader
        def load_user(user_id):
            user = db.session.get(User, int(user_id))
            if user is None:
                return None
            if user.role == 'teacher':
                return db.session.get(Teacher, user_id)
            elif user.role == 'student':
                return db.session.get(Student, user_id)
            return user

    from .views import views
    from .auth import auth
    from website.function.command import command
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(command, url_prefix='/')

    return app

