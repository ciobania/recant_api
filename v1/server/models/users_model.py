#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'

import jwt

from base64 import b64encode
from datetime import datetime, timedelta
from flask_security import UserMixin
from uuid import NAMESPACE_DNS, uuid5, UUID
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_auth.v1.server import app, db_sql, db_mongo
from flask_jwt_auth.v1.server.models import BaseModel, user_roles


class User(BaseModel, UserMixin):
    """
    User Model for storing user related details.
    """
    __tablename__ = 'users'

    email = db_sql.Column(db_sql.String(255), unique=True, nullable=False)
    username = db_sql.Column(db_sql.String(255), unique=True, nullable=True)
    password = db_sql.Column(db_sql.String(255), nullable=False)
    registered_on = db_sql.Column(db_sql.DateTime, nullable=False)
    admin = db_sql.Column(db_sql.Boolean, nullable=False, default=False)
    roles = db_sql.relationship('Role', secondary=user_roles,
                                backref=db_sql.backref('users', lazy='joined'))
    SALT = app.config.get('SECRET_KEY').encode()

    def __init__(self, email, password, username=None, is_admin=False, roles=('basic',)):
        super().__init__()
        self.email = email
        self.password = self.generate_password_hash(password)
        self.registered_on = datetime.now()
        self.is_admin = is_admin
        # TODO: should I add a try/except for TypeError: Incompatible collection type: tuple is not list-like?
        # TODO: should I make changes into API endpoint to guard against parameter validation
        # TODO: should I guard against above error inside the Model and back-propagate the error?
        self.roles = roles
        if username:
            self.username = username
        if self.auto_save:
            self.save()

    def generate_password_hash(self, password):
        self._gen_password_hash(password)
        return self.password_hash

    def check_password_hash(self, password):
        self._gen_password_hash(password)
        return check_password_hash(self.password, b64encode(password.encode()).decode())

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth token.
        :param user_id: ID of User
        :return: string
        """
        try:
            payload = {'exp': datetime.utcnow() + timedelta(seconds=app.config.get('JWT_TTL')),
                       'iat': datetime.utcnow(),
                       'sub': user_id.hex}
            return jwt.encode(payload,
                              app.config.get('SECRET_KEY'),
                              algorithm='HS256')
        except Exception as _:
            err_msg = 'exception_in uui:: {}'.format(_)
            return err_msg

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
                                 app.config.get('SECRET_KEY'),
                                 algorithms=['HS256', ])
            token_is_blacklisted = BlacklistToken.check_blacklist(auth_token)
            if token_is_blacklisted:
                err_msg = err_msg.format('Token is blacklisted.')
            else:
                return UUID(payload['sub'])
        except jwt.ExpiredSignatureError as _:
            err_msg = err_msg.format('Signature expired.')
        except jwt.InvalidTokenError as _:
            err_msg = err_msg.format('Invalid token.')
        else:
            err_msg = err_msg.format('Unknown error whilst decoding token.')

        return err_msg

    def _gen_password_hash(self, password):
        self.password_hash = generate_password_hash(b64encode(password.encode()).decode())


class Base(db_mongo.Document):
    meta = {'db_alias': 'tokens',
            'collection': 'blacklist_tokens',
            'allow_inheritance': True}

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
        encoded_bytes = b64encode(data_to_encode)
        encoded_str = str(encoded_bytes, "utf-8")

        return encoded_str

    @staticmethod
    def check_blacklist(auth_token):
        response = BlacklistToken.objects.filter(token=auth_token)
        if response:
            return True
        else:
            return False
