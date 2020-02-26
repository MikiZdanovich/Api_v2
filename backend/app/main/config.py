import os

# uncomment the line below for postgres database url from environment variable
basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = os.environ['DATABASE_URL']


class Config:
    # uncomment the line below and set up Secret_key
    # SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    DATABASE_URI = postgres_local_base
    DEBUG = True
    # uncomment line below to use sqlite db
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
    CELERY_RESULT_BACKEND = 'rpc://'


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

# key = Config.SECRET_KEY
