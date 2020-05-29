# project/server/tests/base.py


from flask_testing import TestCase

from flask_jwt_auth.v1.server import app, db_sql


class BaseTestCase(TestCase):
    """
    Base Tests
    """

    def create_app(self):
        app.config.from_object('flask_jwt_auth.v1.server.config.TestingConfig')
        return app

    def setUp(self):
        if app.config.get('DEBUG') and app.config.get('TESTING'):
            formatter = '\t|{:<32}|{:<15}|{:<5}|'
            print('\nConnecting to:: ')
            print(formatter.format('db_name', 'host', 'port'), sep='\t\t\t')
            print(formatter.format(db_sql.engine.url.database,
                                   db_sql.engine.url.host,
                                   db_sql.engine.url.port), sep='\t\t')

        db_sql.create_all()
        db_sql.session.commit()

    def tearDown(self):
        db_sql.session.remove()
        db_sql.drop_all()
        db_sql.session.commit()
