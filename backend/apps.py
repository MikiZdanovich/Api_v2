from celery import Celery
from flask import Flask

from app.main.config import config_by_name
from app.main.views import user_bp
from database import db


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    with app.app_context():
        register_blueprints(app)
    return app


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        include='app.main.service.get_repositories_service'
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_celery_app(config):
    app = create_app(config)
    celery = make_celery(app)
    return celery


def register_blueprints(app):
    app.register_blueprint(user_bp)
