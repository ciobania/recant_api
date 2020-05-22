#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
import json
import unittest
from time import sleep

from flask_jwt_auth.v1.server import db_sql
from flask_jwt_auth.v1.server.models import User, BlacklistToken
from flask_jwt_auth.v1.tests.base import BaseTestCase


class TestAuthBlueprint(BaseTestCase):
    auth = None

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_can_get_a_grocery_list(self):
        """
        Test can successfully get a grocery list.
        """
        with self.client:
            response = self.client.get('/groceries',
                                       data='',
                                       content_type='application/json')
            print('test_can_get_a_grocery_list:: \n', response.data.decode())

            self.assertTrue(response)
            # self.assertTrue(data['status'] == 'success')
            # self.assertTrue(data['message'] == 'Successfully registered.')
            # self.assertTrue(data['auth_token'])
            # self.assertTrue(data['content_type'] == 'application/json')
            # self.assertEqual(data['status_code'], 201)
