#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'

import unittest

from flask_jwt_auth.v1.server import db_sql
from flask_jwt_auth.v1.server.models import User
from flask_jwt_auth.v1.server.models.roles_model import Role
from flask_jwt_auth.v1.tests.base_test_case import BaseTestCase


class TestUserModel(BaseTestCase):
    session = None
    meta = None

    def setUp(self):
        super(TestUserModel, self).setUp()
        print('\nConnecting to DB:', db_sql.engine.url.database)
        self.session = db_sql.session
        self.meta = db_sql.metadata

    def tearDown(self):
        super(TestUserModel, self).tearDown()

    def test_encode_auth_token(self):
        """
        Test can encode auth token.
        """
        role = Role('admin')
        user = User(email='test@test.com',
                    password='test',
                    roles=[role])
        user.save()
        auth_token = user.encode_auth_token(user_id=user.id)
        self.assertTrue(isinstance(auth_token, bytes),
                        msg='auth_token type is:: {} and value:: {}'.format(type(auth_token), auth_token))
        decoded_auth_token = User.decode_auth_token(auth_token=auth_token.decode('utf-8'))
        self.assertTrue(decoded_auth_token == user.id,
                        msg='Received:: {} - {}'.format(type(decoded_auth_token), type(user.id)))


if __name__ == '__main__':
    unittest.main()
