# manage.py


import os
import unittest
import coverage

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from flask_jwt_auth.v1.server import app, db_sql, models


COV = coverage.coverage(
    branch=True,
    include='v1/*',
    omit=[
        'v1/tests/*',
        'v1/server/config.py',
        'v1/server/*/__init__.py'
    ]
)
COV.start()


manager = Manager(app)
migrate = Migrate(app, db_sql)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('v1/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('v1/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


@manager.command
def create_db():
    """Creates the db tables."""
    db_sql.create_all()
    db_sql.session.commit()


@manager.command
def drop_db():
    """Drops the db tables."""
    db_sql.drop_all()


if __name__ == '__main__':
    manager.run()
