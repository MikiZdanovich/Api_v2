import os

from celery import Celery

app = Celery(
    broker=os.environ.get('CELERY_BROKER_URL'),
    backend=os.environ.get('CELERY_BACKEND_URL')
)
