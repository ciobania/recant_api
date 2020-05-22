# project/server/tests/test_config.py
import unittest

from flask import current_app
from flask_testing import TestCase

from flask_jwt_auth.v1.server import app


DATABASE_URI = 'postgresql://es_user:es_password@192.168.1.133:54320/{}'


class TestDevelopmentConfig(TestCase):
    """
    Test DevelopmentConfig works correctly.
    """
    def create_app(self):
        app.config.from_object('v1.server.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        """
        Test app is development when config is: DevelopmentConfig.
        """
        self.assertFalse(app.config['SECRET_KEY'] == 'some_precious_secret_key_that_is_long')
        self.assertTrue(app.config['DEBUG'])
        self.assertFalse(current_app is None)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == DATABASE_URI.format('flask_jwt_auth'))


class TestTestingConfig(TestCase):
    """
    Test application TestingConfig works correctly.
    """
    def create_app(self):
        app.config.from_object('v1.server.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        """
        Test app is testing when config is: TestingConfig.
        """
        self.assertFalse(app.config['SECRET_KEY'] == 'some_precious_secret_key_that_is_long')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == DATABASE_URI.format('flask_jwt_auth_test'))


class TestProductionConfig(TestCase):
    """
    Test application ProductionConfig works correctly.
    """
    def create_app(self):
        app.config.from_object('v1.server.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        """
        Test app is production when config is: ProductionConfig.
        """
        self.assertTrue(app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()
