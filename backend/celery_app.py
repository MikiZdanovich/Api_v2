import os
from celery import Celery

app = Celery('app',
             broker=os.environ.get('CELERY_BROKER_URL'),
             backend=os.environ.get('CELERY_BACKEND_URL'),
             include='app.main.service.get_repositories_service'
             )
app.config_from_object("celery_q.celeryconfig")
