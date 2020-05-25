#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
import json
from uuid import UUID

from flask import g

from flask_jwt_auth.v1.server.models import User
from flask_jwt_auth.v1.tests.base import BaseTestCase
from flask_jwt_auth.v1.tests.user_auth_ep_tests.auth_helpers import AuthHelpers


class TestGroceriesBlueprint(BaseTestCase):
    auth = None

    def setUp(self):
        self.auth = AuthHelpers(self.client)

    def tearDown(self):
        pass

    def test_can_get_a_grocery_list(self):
        """
        Test can successfully get a grocery list.
        """
        user_payload = {'email': 'grocery_list_get@mailinator.com',
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

            data = self.auth._request('/groceries', 'get', auth_token=data['auth_token'])
            self.assertTrue(data['name'] == 'Grocery List 1')
            self.assertTrue(isinstance(data['id'], str))
            self.assertTrue(data['total_items'] == 10)
            print('grocery_list_data', data, '\n')
            print('g.user is::', g.user)

    def test_cannot_get_grocery_list_without_login(self):
        """
        Test grocery list endpoint is not accessible without login.
        """
        with self.client:
            response = self.client.get('/groceries',
                                       data='',
                                       content_type='application/json')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertEqual(response.status_code, 403)
