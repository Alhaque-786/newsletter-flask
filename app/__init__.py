from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from redis import Redis
from config import Config

db = SQLAlchemy()
mail = Mail()
redis_client = Redis.from_url(Config.REDIS_URL)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from . import routes
        db.create_all()

    return app
