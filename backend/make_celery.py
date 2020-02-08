import os
from apps import create_celery_app


celery = create_celery_app(os.getenv('BOILERPLATE_ENV') or 'dev')