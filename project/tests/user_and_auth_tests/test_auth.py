#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
import unittest
from time import sleep

from flask_jwt_auth.project.server import db_sql
from flask_jwt_auth.project.server.models import User, BlacklistToken
from flask_jwt_auth.project.tests.base import BaseTestCase
from flask_jwt_auth.project.tests.user_and_auth_tests.auth_helpers import AuthHelpers


class TestAuthBlueprint(BaseTestCase):
    auth = None

    def setUp(self):
        self.auth = AuthHelpers(self.client)

    def tearDown(self):
        pass

    def test_registration(self):
        """
        Test for User registration.
        """
        user_payload = {'email': 'adrian_paul@mailinator.com',
                        'password': '1234567890'}
        with self.client:
            data = self.auth.register_user(user_payload=user_payload)

            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(data['content_type'] == 'application/json')
            self.assertEqual(data['status_code'], 201)

    def test_user_registering_with_already_registered_user_email_fails(self):
        """
        Test that registration with an existing email address is not possible.
        """
        user_payload = {'email': 'joe@mailinator.com',
                        'password': '1234567890'}
        user = User(**user_payload)
        db_sql.session.add(user)
        db_sql.session.commit()
        with self.client:
            data = self.auth.register_user(user_payload=user_payload)
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User already exists. Please Log In.',
                            msg='Received: {}'.format(data['message']))
            self.assertTrue(data['content_type'] == 'application/json')
            self.assertEqual(data['status_code'], 202)

    def test_that_a_registered_user_can_login(self):
        """
        Test registered-user can login.
        """
        user_payload = {'email': 'some_email@mailinator.com',
                        'password': '1234567890'}
        with self.client:
            data = self.auth.register_user(user_payload=user_payload)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(data['content_type'] == 'application/json')
            self.assertEqual(data['status_code'], 201)

            data = self.auth.login_user(user_payload)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(data['content_type'] == 'application/json')
            self.assertEqual(data['status_code'], 200)

    def test_registered_user_cannot_login_with_wrong_password(self):
        """
        Test registered-user cannot login with wrong password.
        """
        user_payload = {'email': 'wrong_password@mailinator.com',
                        'password': '1234567890'}
        with self.client:
            data = self.auth.register_user(user_payload=user_payload)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(data['content_type'] == 'application/json')
            self.assertEqual(data['status_code'], 201)

            # login
            user_payload['password'] = '123456789'
            data = self.auth.login_user(user_payload)
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Incorrect password.')
            self.assertFalse(data.get('auth_token'))
            self.assertTrue(data['content_type'] == 'application/json')
            self.assertEqual(data['status_code'], 400)

    def test_non_registered_user_cannot_login(self):
        """
        Test that a non-registered user cannot login.
        """
        user_payload = {'email': 'non_registered_email@mailinator.com',
                        'password': 'non_essential_password'}
        with self.client:
            data = self.auth.login_user(user_payload)

            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertTrue(data['content_type'] == 'application/json')
            self.assertEqual(data['status_code'], 404)

    def test_user_token_status_is_sent_in_the_request(self):
        """
        Test user token status is sent in the request.
        """
        user_payload = {'email': 'token_sent@mailinator.com',
                        'password': '1234567890'}
        with self.client:
            data = self.auth.register_user(user_payload=user_payload)
            data = self.auth.auth_status(auth_token=data['auth_token'])

            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['email'] == user_payload['email'])
            self.assertTrue(data['data']['admin'] == 'true' or 'false')
            self.assertTrue(data['content_type'] == 'application/json')
            self.assertEqual(data['status_code'], 200)

    def test_registered_user_can_logout_before_token_expires(self):
        """
        Test that a registered user can logout before token expires.
        """
        user_payload = {'email': 'registered_and_valid_token@mailinator.com',
                        'password': '1234567890'}
        with self.client:
            data = self.auth.register_user(user_payload=user_payload)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue('auth_token' in data and data['auth_token'])
            self.assertTrue(data['content_type'] == 'application/json')
            self.assertEqual(data['status_code'], 201)

            data = self.auth.login_user(user_payload=user_payload)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(data['content_type'] == 'application/json')
            self.assertEqual(data['status_code'], 200)

            data = self.auth.logout_user(auth_token=data['auth_token'])
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(data['status_code'], 200)

    def test_registered_user_cannot_logout_with_invalid_token(self):
        """
        Test that a registered user cannot logout after token has expired.
        """
        user_payload = {'email': 'logout_with_expired_token@mailinator.com',
                        'password': '0123456789'}
        with self.client:
            data = self.auth.register_user(user_payload=user_payload)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue('auth_token' in data and data['auth_token'])
            self.assertTrue(data['content_type'] == 'application/json')
            self.assertEqual(data['status_code'], 201)

            data = self.auth.login_user(user_payload=user_payload)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(data['content_type'] == 'application/json')
            self.assertEqual(data['status_code'], 200)

            sleep(6)
            data = self.auth.logout_user(auth_token=data['auth_token'])
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Signature expired. Please Log In again.')
            self.assertEqual(data['status_code'], 401)

    def test_registered_user_cannot_logout_with_blacklisted_token(self):
        """
        Test that a registered user cannot logout with a blacklisted token.
        """
        user_payload = {'email': 'blacklisted_token_logout@mailinator.com',
                        'password': '12345678900'}
        with self.client:
            data = self.auth.register_user(user_payload=user_payload)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(data['content_type'] == 'application/json')
            self.assertEqual(data['status_code'], 201)

            data = self.auth.login_user(user_payload=user_payload)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(data['content_type'] == 'application/json')
            self.assertEqual(data['status_code'], 200)
            # blacklist a valid token
            blacklist_token = BlacklistToken(token=data['auth_token'])
            blacklist_token.save()

            # blacklisted valid token logout
            data = self.auth.logout_user(auth_token=data['auth_token'])
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Token is blacklisted. Please Log In again.')
            self.assertEqual(data['status_code'], 401)

    def test_user_auth_status_with_a_valid_blacklisted_token(self):
        """
        Test User auth status with a blacklisted valid token.
        """
        user_payload = {'email': 'valid_blacklisted_toke@mailinator.com',
                        'password': '1234567890'}
        with self.client:
            data = self.auth.register_user(user_payload=user_payload)
            blacklist_token = BlacklistToken(token=data['auth_token'])
            blacklist_token.save()

            data = self.auth.auth_status(auth_token=data['auth_token'])

            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Token is blacklisted. Please Log In again.')
            self.assertEqual(data['status_code'], 401)


if __name__ == '__main__':
    unittest.main()
