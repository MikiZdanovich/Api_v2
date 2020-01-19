from celery_app import app as celery

@celery.task
def task():
    return "hello"

