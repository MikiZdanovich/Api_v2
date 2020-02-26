import os

from celery import Celery
from flask import Flask

from app.main.config import config_by_name
from database import configure_engine, metadata

engine = configure_engine(os.getenv('DATABASE_URL'))


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    metadata.bind = engine
    with app.app_context():
        return app


def celery_make(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        include='app.main.service.user_service'
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
    celery = celery_make(app)
    return celery
