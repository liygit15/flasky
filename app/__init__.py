from flask import Flask
from .db import db, migrate
from .models.cat import Cat
from .models.dog import Dog
from .routes.cat_routes import cats_bp 
from .routes.dog_routes import dogs_bp
import os

def create_app(config = None):
    # __name__ stores the name of the module we're in
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    db.init_app(app)
    migrate.init_app(app, db)

    if config:
        app.config.update(config)

    app.register_blueprint(cats_bp)
    app.register_blueprint(dogs_bp)

    return app


