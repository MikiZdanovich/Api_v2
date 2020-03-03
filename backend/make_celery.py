import os

from backend.apps import create_celery_app

celery = create_celery_app(os.getenv('BOILERPLATE_ENV') or 'dev')

if __name__ == "__main__":
    celery.run()
