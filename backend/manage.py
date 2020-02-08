from __future__ import absolute_import
import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from apps import create_app
from database import db

application = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')


application.app_context().push()

manager = Manager(application)

migrate = Migrate(application, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    application.run()


@manager.command
def create_db():
    with application.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
