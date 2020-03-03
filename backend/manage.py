import os

from flask_script import Manager

from backend.app.main.model.users import metadata
from backend.app.main.views import user_bp
from backend.apps import create_app

application = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
application.register_blueprint(user_bp)

application.app_context().push()

manager = Manager(application)


@manager.command
def run():
    application.run()


@manager.command
def create_db():
    metadata.drop_all()
    metadata.create_all()


if __name__ == '__main__':
    manager.run()
