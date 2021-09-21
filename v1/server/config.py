# project/server/config.py
import os


class BaseConfig:
    """
    Base configuration.
    """
    HOST_IP = os.getenv('HOST_IP')
    APP_SETTINGS = os.getenv('APP_SETTINGS')
    ENV = os.getenv('FLASK_ENV')
    DEBUG = os.getenv('DEBUG')
    SECRET_KEY = os.getenv('SECRET_KEY', 'some_precious_secret_key_that_is_long')
    POSTGRES_LOCAL_BASE = 'postgresql://es_user:es_password@{}:54320/'.format(HOST_IP)

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
    """
    Development configuration.
    """
    BCRYPT_LOG_ROUNDS = 4
    DATABASE_NAME = 'flask_jwt_auth'
    POSTGRES_LOCAL_BASE = 'postgresql://es_user:es_password@{}:54320/'.format(BaseConfig.HOST_IP)
    SQLALCHEMY_DATABASE_URI = POSTGRES_LOCAL_BASE + DATABASE_NAME


class TestingConfig(BaseConfig):
    """
    Testing configuration.
    """
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    DATABASE_NAME = 'flask_jwt_auth_test'
    POSTGRES_LOCAL_BASE = 'postgresql://es_user:es_password@{}:54320/'.format(BaseConfig.HOST_IP)
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
        'host': 'mongodb://bt_user:bt_password@{}:27017/tokens?authSource=admin'.format(BaseConfig.HOST_IP)}
    MONGODB_DB = 'tokens'
    MONGODB_HOST = BaseConfig.HOST_IP
    MONGODB_PORT = 27017
    MONGODB_USERNAME = 'bt_user'
    MONGODB_PASSWORD = 'bt_password'


class ProductionConfig(BaseConfig):
    """
    Production configuration.
    """
    ENV = 'production'
    SECRET_KEY = 'my_precious'
    DEBUG = False
    DATABASE_NAME = 'flask_jwt_auth_prod'
    POSTGRES_LOCAL_BASE = 'postgresql://es_user:es_password@{}:54320/'.format(BaseConfig.HOST_IP)
    SQLALCHEMY_DATABASE_URI = POSTGRES_LOCAL_BASE + DATABASE_NAME
    MONGODB_SETTINGS = {'db': 'tokens',
                        'host': BaseConfig.HOST_IP,
                        'port': 27017,
                        'username': 'bt_user',
                        'password': 'bt_password'}
