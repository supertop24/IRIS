import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
def create_app(config_class='config.DevelopmentConfig'):  # Default to DevelopmentConfig
    app = Flask(__name__)
    app.config.from_object(config_class)  # Load the configuration
    db.init_app(app)  # Initialize SQLAlchemy
    from website import models
    with app.app_context():
        db.create_all()

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app