# project/server/tests/base.py


from flask_testing import TestCase

from flask_jwt_auth.v1.server import app, db_sql


class BaseTestCase(TestCase):
    """
    Base Tests
    """

    def create_app(self):
        app.config.from_object('v1.server.config.TestingConfig')
        return app

    def setUp(self):
        db_sql.create_all()
        db_sql.session.commit()

    def tearDown(self):
        db_sql.session.remove()
        db_sql.drop_all()
