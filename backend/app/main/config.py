import os

# uncomment the line below for postgres database url from environment variable
basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = os.environ['DATABASE_URL']
postgres_local_test_base = os.environ['TEST_BASE']


class Config:
    # uncomment the line below and set up Secret_key
    # SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
    CELERY_RESULT_BACKEND = 'rpc://'
    TEST_DATABASE_URI = postgres_local_test_base


class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

# key = Config.SECRET_KEY
