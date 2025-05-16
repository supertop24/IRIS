import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD
=======

>>>>>>> 380d5eaed79c54fa9512edb04e14be2db475209e

db = SQLAlchemy()
def create_app(config_class='website.config.DevelopmentConfig'):
    app=Flask(__name__)
    app.config.from_object(config_class)

    # Initialize the db with the app
    db.init_app(app)
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    if not os.path.exists(os.path.join(BASEDIR, 'database.db')):
        with app.app_context():
            db.create_all()  # Create tables in the database



    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app