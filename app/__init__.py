import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import logging
from datetime import timedelta

db = SQLAlchemy()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)
talisman = Talisman()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    load_dotenv()

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    db.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    
    # Initialize SSLify within the application context
    from flask_sslify import SSLify
    sslify = SSLify(app)

    talisman.init_app(app, content_security_policy={
        'default-src': '\'self\'',
        'img-src': '*',
        'style-src': ['\'self\'', 'https://fonts.googleapis.com'],
        'font-src': ['\'self\'', 'https://fonts.gstatic.com']
    })
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

    from .routes import main
    app.register_blueprint(main)

    from .errors import errors
    app.register_blueprint(errors)

    return app