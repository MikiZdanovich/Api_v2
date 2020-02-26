import os

from flask_script import Manager

from apps import create_app
from app.main.model.users import metadata
from app.main.views import user_bp

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


#миграции через Алембик , LiquiBase (вариант когда заебет алембик)


# @manager.command
# def test():
#     """Runs the unit tests."""
#     tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
#     result = unittest.TextTestRunner(verbosity=2).run(tests)
#     if result.wasSuccessful():
#         return 0
#     return 1


if __name__ == '__main__':
    manager.run()
