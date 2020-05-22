#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'

import base64
import jwt
from datetime import datetime, timedelta
from uuid import NAMESPACE_DNS, uuid5

from flask_jwt_auth.project.server import app, db_sql, bcrypt, db_mongo


class User(db_sql.Model):
    """
    User Model for storing user related details.
    """
    __tablename__ = 'users'

    id = db_sql.Column(db_sql.Integer, primary_key=True, autoincrement=True)
    email = db_sql.Column(db_sql.String(255), unique=True, nullable=False)
    password = db_sql.Column(db_sql.String(255), nullable=False)
    registered_on = db_sql.Column(db_sql.DateTime, nullable=False)
    admin = db_sql.Column(db_sql.Boolean, nullable=False, default=False)

    def __init__(self, email, password, is_admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(password, app.config.get('BCRYPT_LOG_ROUNDS')).decode()
        self.registered_on = datetime.now()
        self.is_admin = is_admin

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth token.
        :param user_id: ID of User
        :return: string
        """
        try:
            payload = {'exp': datetime.utcnow() + timedelta(days=0, seconds=5),
                       'iat': datetime.utcnow(),
                       'sub': user_id}
            return jwt.encode(payload,
                              app.config.get('SECRET_KEY'),
                              algorithm='HS256')
        except Exception as _:
            return _

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token.
        :param auth_token:
        :return: integer|string
        """
        err_msg = '{} Please Log In again.'
        try:
            payload = jwt.decode(auth_token,
                                 app.config.get('SECRET_KEY'))
            token_is_blacklisted = BlacklistToken.check_blacklist(auth_token)
            if token_is_blacklisted:
                err_msg = err_msg.format('Token is blacklisted.')
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError as _:
            err_msg = err_msg.format('Signature expired.')
        except jwt.InvalidTokenError as _:
            err_msg = err_msg.format('Invalid token.')
        else:
            err_msg = err_msg.format('Unknown error whilst decoding token.')

        return err_msg


class Base(db_mongo.Document):
    meta = {'db_alias': 'tokens',
            'collection': 'blacklist_tokens',
            'allow_inheritance': True}

    # _id = db_mongo.UUIDField(required=True,
    #                          primary_key=True)
    created_at = db_mongo.DateTimeField(default=datetime.now, required=True)
    written_at = db_mongo.DateTimeField(default=datetime.now, required=True)


class BlacklistToken(db_mongo.Document):
    token = db_mongo.StringField(required=True)
    id = db_mongo.UUIDField(required=True,
                            primary_key=True)

    def __init__(self, token, *args, **values):
        super().__init__(*args, **values)
        self.id = uuid5(NAMESPACE_DNS,
                        self._encode_data(token))
        self.token = token
        self.blacklisted_on = db_mongo.DateTimeField(default=datetime.now, required=True)

    def __str__(self):
        if hasattr(self, 'id'):
            return f'<{type(self).__name__}:: {self.token}>'
        else:
            return '<{}>'.format(type(self).__name__)

    @staticmethod
    def _encode_data(data):
        data_to_encode = '.'.join(data).encode("utf-8")
        encoded_bytes = base64.b64encode(data_to_encode)
        encoded_str = str(encoded_bytes, "utf-8")

        return encoded_str

    @staticmethod
    def check_blacklist(auth_token):
        response = BlacklistToken.objects.filter(token=auth_token)
        if response:
            return True
        else:
            return False
