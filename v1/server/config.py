# project/server/config.py

import os
HOST_IP = '192.168.1.137'
# HOST_IP = '192.168.1.133'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
POSTGRES_LOCAL_BASE = 'postgresql://es_user:es_password@{}:54320/'.format(HOST_IP)


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'some_precious_secret_key_that_is_long')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # MONGODB_SETTINGS = {'db': 'tokens',
    #                     'host': '192.168.1.133',
    #                     'port': 27017,
    #                     'username': 'bt_user',
    #                     'password': 'bt_password'}
    MONGODB_SETTINGS = {
        'db': 'tokens',
        'host': 'mongodb://bt_user:bt_password@{}:27017/tokens?authSource=admin'.format(HOST_IP)}
    MONGODB_DB = 'tokens'
    MONGODB_HOST = HOST_IP
    MONGODB_PORT = 27017
    MONGODB_USERNAME = 'bt_user'
    MONGODB_PASSWORD = 'bt_password'


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    ENV = 'development'
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    DATABASE_NAME = 'flask_jwt_auth'
    SQLALCHEMY_DATABASE_URI = POSTGRES_LOCAL_BASE + DATABASE_NAME


class TestingConfig(BaseConfig):
    """Testing configuration."""
    ENV = 'testing'
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    DATABASE_NAME = 'flask_jwt_auth_test'
    SQLALCHEMY_DATABASE_URI = POSTGRES_LOCAL_BASE + DATABASE_NAME
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    # MONGODB_SETTINGS = {
    #                     'db': 'tokens',
    #                     'host': '192.168.1.133',
    #                     'port': 27017,
    #                     'username': 'bt_user',
    #                     'password': 'bt_password'}
    # TODO: need to sort out why I use the tokens, and where I use the postgresql
    MONGODB_SETTINGS = {
        'db': 'tokens',
        'host': 'mongodb://bt_user:bt_password@{}:27017/tokens?authSource=admin'.format(HOST_IP)}
    MONGODB_DB = 'tokens'
    MONGODB_HOST = HOST_IP
    MONGODB_PORT = 27017
    MONGODB_USERNAME = 'bt_user'
    MONGODB_PASSWORD = 'bt_password'


class ProductionConfig(BaseConfig):
    """Production configuration."""
    ENV = 'production'
    SECRET_KEY = 'my_precious'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql:///example'
    MONGODB_SETTINGS = {'db': 'tokens',
                        'host': HOST_IP,
                        'port': 27017,
                        'username': 'bt_user',
                        'password': 'bt_password'}
