# project/server/tests/base.py
import os

from dotenv import load_dotenv
from flask_testing import TestCase

from flask_jwt_auth.v1.server import app, db_sql, BASE_DIR


class BaseTestCase(TestCase):
    """
    Base Tests
    """

    def create_app(self):
        app_cfg_obj = os.getenv('APP_SETTINGS', 'flask_jwt_auth.v1.server.config.TestingConfig')
        app.config.from_object(app_cfg_obj)
        return app

    def setUp(self):
        # this load_dotenv does not work, need to revisit to refactor one single configurable .env
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
        # pass
