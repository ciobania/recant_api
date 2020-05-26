#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
import json
import unittest
from uuid import uuid5, NAMESPACE_DNS, UUID

from flask import g

from flask_jwt_auth.v1.server import db_sql
from flask_jwt_auth.v1.tests.base import BaseTestCase
from flask_jwt_auth.v1.tests.user_auth_ep_tests.auth_helpers import AuthHelpers


class TestGroceriesBlueprint(BaseTestCase):
    auth = None
    user_data = None
    should_register_and_login = False

    def setUp(self):
        self.auth = AuthHelpers(self.client)
        print('\nConnecting to DB:', db_sql.engine.url.database)
        self.session = db_sql.session
        self.meta = db_sql.metadata
        clear_db_data(self.session, self.meta)

    def tearDown(self):
        clear_db_data(self.session, self.meta)

    def register_and_login(self, email):
        user_payload = {'email': '{}@mailinator.com'.format(email),
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

            self.user_data = data

    def test_can_get_all_grocery_list(self):
        """
        Test can successfully get all grocery lists.
        """
        self.register_and_login(email='grocery_list_user')
        with self.client:
            req_response = self.auth.rh.request('/api/groceries/',
                                                'get',
                                                auth_token=self.user_data['auth_token'])

            print('\n', req_response, '\n')
            self.assertTrue(req_response['data'][0]['name'] == 'Grocery List 1')
            self.assertTrue(req_response['data'][0]['description'] == 'A first grocery list 1.')
            self.assertTrue(req_response['data'][0]['created_by'] == 10003)
            self.assertTrue(req_response['data'][0]['total_items'] == 10)
            self.assertTrue(isinstance(req_response['data'][0]['id'], UUID))

    def test_cannot_get_grocery_list_without_login(self):
        """
        Test grocery list endpoint is not accessible without login.
        """
        with self.client:
            response = self.client.get('/api/groceries',
                                       data='',
                                       content_type='application/json')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Provide a valid auth token.')
            self.assertEqual(response.status_code, 403)

    def test_can_create_grocery_list(self):
        """
        Test that can create a grocery list.
        """
        grocery_list_payload = {'name': 'Grocery List 2',
                                'description': 'List of 2020'}
        self.register_and_login(email='grocery_create_list_user')
        with self.client:
            data = self.auth.rh.request('/api/groceries',
                                        'post',
                                        auth_token=self.user_data['auth_token'],
                                        payload=grocery_list_payload)
            self.assertTrue(data['name'] == grocery_list_payload['name'],
                            msg='Received: {}'.format(data['name']))
            self.assertTrue(data['description'] == grocery_list_payload['description'],
                            msg='Received: {}'.format(data['name']))
            self.assertTrue(isinstance(data['id'], str))
            self.assertTrue(data['total_items'] == 0)
            self.assertTrue(data['created_by'] == g.user.id)

    def test_can_update_a_grocery_list(self):
        """
        Test that can update a grocery list.
        """
        grocery_list_payload = {'name': 'Grocery List update',
                                'description': 'List of 2020 updated'}
        self.register_and_login(email='grocery_update_list_user')
        with self.client:
            data = self.auth.rh.request('/api/groceries/{}'.format(uuid5(NAMESPACE_DNS,
                                                                         grocery_list_payload['name'])),
                                        'post',
                                        auth_token=self.user_data['auth_token'],
                                        payload=grocery_list_payload)
            self.assertTrue(data['name'] == grocery_list_payload['name'],
                            msg='Received: {}'.format(data['name']))
            self.assertTrue(data['description'] == grocery_list_payload['description'],
                            msg='Received: {}'.format(data['name']))
            self.assertTrue(isinstance(data['id'], str))
            self.assertTrue(data['total_items'] == 14)

    def test_can_delete_a_grocery_list(self):
        """
        Test that can delete a grocery list.
        """
        grocery_list_payload = {'name': 'Grocery List delete'}
        self.register_and_login(email='grocery_delete_list_user')
        with self.client:
            list_uuid = uuid5(NAMESPACE_DNS,
                              grocery_list_payload['name'])
            data = self.auth.rh.request('/api/groceries/{}'.format(list_uuid),
                                        'delete',
                                        auth_token=self.user_data['auth_token'])
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Grocery List with id: {} was deleted.'.format(list_uuid))


def clear_db_data(session, meta):
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        session.execute(table.delete())
    session.commit()


if __name__ == '__main__':
    unittest.main()
