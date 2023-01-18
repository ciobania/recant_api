#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
import json
import unittest

from flask_jwt_auth.v1.server.models import GroceriesList, User
from flask_jwt_auth.v1.tests.base_test_case import BaseTestCase
from flask_jwt_auth.clients.groceries_helpers import GroceriesHelpers
from flask_jwt_auth.clients.auth_helpers import AuthHelpers


class TestGroceriesBlueprint(BaseTestCase):
    auth = None
    user_data = None
    gls = []
    should_register_and_login = False

    def setUp(self):
        super(TestGroceriesBlueprint, self).setUp()
        self.auth = AuthHelpers(self.client)
        self.gh = GroceriesHelpers(self.client)
        self.gls = []

    def tearDown(self):
        super(TestGroceriesBlueprint, self).tearDown()
        # pass

    def add_groceries_lists(self, grocery_list_name, user_data):
        print(f'{user_data=}')
        for idx in range(5):
            grocery_list_payload = {'name': f'Grocery List {idx} - {grocery_list_name}',
                                    'description': f'Description for Grocery List {idx}'}
            data = self.gh.create_grocery_list(auth_token=user_data['auth_token'],
                                               payload=grocery_list_payload)
            print(f'{data=}')
            self.gls.append(data['data'])

    def register_and_login(self, email):
        user_payload = {'email': '{}@mailinator.com'.format(email),
                        'password': '1234567890'}
        with self.client:
            registered_data = self.auth.register_user(user_payload=user_payload)
            print('registered_data::', registered_data)
            self.assertTrue(registered_data['status'] == 'success', msg=f'Status is: {registered_data["status"]}')
            self.assertTrue(registered_data['message'] == 'Successfully registered.')
            self.assertTrue(registered_data['auth_token'])
            self.assertTrue(registered_data['content_type'] == 'application/json')
            self.assertEqual(registered_data['status_code'], 201)

            login_data = self.auth.login_user(user_payload)
            print('login_data::', login_data)
            self.assertTrue(login_data['status'] == 'success')
            self.assertTrue(login_data['message'] == 'Successfully logged in.')
            self.assertTrue(login_data['auth_token'])
            self.assertTrue(login_data['content_type'] == 'application/json')
            self.assertEqual(login_data['status_code'], 200)

            response_object = {'auth_token': login_data['auth_token'],
                               'user_data': User.query.filter_by(email=user_payload['email']).first().as_dict()}
            return response_object

    def test_can_get_all_grocery_list(self):
        """
        Test can successfully get all grocery lists.
        """
        user_auth = self.register_and_login(email='can_get_all_grocery_lists')
        self.add_groceries_lists(grocery_list_name='can_get_all_grocery_lists', user_data=user_auth)
        with self.client:
            req_response = self.gh.get_all_grocery_lists(auth_token=user_auth['auth_token'])
            self.assertEqual(len(req_response['data']), len(self.gls),
                             msg='\nReceived:: {}\nExpected:: {}'.format(len(req_response['data']), len(self.gls)))
            self.assertTrue(req_response['data'][0]['name'] == self.gls[0]['name'],
                            msg='\nReceived:: {}\nExpected:: {}'.format(req_response['data'][0]['name'],
                                                                        self.gls[0]['name']))
            self.assertTrue(req_response['data'][0]['description'] == self.gls[0]['description'],
                            msg='\nReceived:: {}\nExpected:: {}'.format(req_response['data'][0]['description'],
                                                                        self.gls[0]['description']))
            self.assertTrue(req_response['data'][0]['id'] == self.gls[0]['id'],
                            msg='\nReceived:: {}\nExpected:: {}'.format(req_response['data'][0]['id'],
                                                                        self.gls[0]['id']))

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
        grocery_list_payload = {'name': 'Grocery List 2 - can_create_grocery_list',
                                'description': 'List of 2020'}
        user_auth = self.register_and_login(email='grocery_create_list_user')
        with self.client:
            data = self.gh.create_grocery_list(auth_token=user_auth['auth_token'],
                                               payload=grocery_list_payload)

            self.assertTrue(data['data']['name'] == grocery_list_payload['name'],
                            msg='Received: {}'.format(data['data']['name']))
            self.assertTrue(data['data']['description'] == grocery_list_payload['description'],
                            msg='Received: {}'.format(data['data']['name']))
            self.assertTrue(isinstance(data['data']['id'], str))

    def test_can_update_a_grocery_list(self):
        """
        Test that can update a grocery list.
        """
        grocery_list_payload = {'name': 'Grocery List update',
                                'description': 'List of 2020 updated'}
        user_auth = self.register_and_login(email='grocery_update_list_user')
        self.add_groceries_lists(grocery_list_name='grocery_update_list_user', user_data=user_auth)
        with self.client:
            data = self.gh.update_grocery_list(auth_token=user_auth['auth_token'],
                                               payload=grocery_list_payload,
                                               gls_id=self.gls[4]['id'])
            self.assertTrue(data['name'] == grocery_list_payload['name'],
                            msg='Received: {}'.format(data['name']))
            self.assertTrue(data['description'] == grocery_list_payload['description'],
                            msg='Received: {}'.format(data['name']))
            self.assertTrue(isinstance(data['id'], str))

    def test_can_delete_a_grocery_list(self):
        """
        Test that can delete a grocery list.
        """
        user_auth = self.register_and_login(email='grocery_delete_list_user')
        self.add_groceries_lists(grocery_list_name='grocery_delete_list_user', user_data=user_auth)
        with self.client:
            gls_id = self.gls[3]['id']
            data = self.gh.delete_grocery_list(auth_token=user_auth['auth_token'], gls_id=gls_id)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Grocery List with id: {} was deleted.'.format(gls_id))

    def test_can_share_groceries_lists_created_by_a_user_with_another_user(self):
        """
        Test that can share a grocery list created by a user with another user.
        """
        grocery_list_payload = {'name': 'Grocery List 2 share with another user',
                                'description': 'List of 2020'}
        user_auth_1 = self.register_and_login(email='grocery_create_list_user_2')
        user_auth_2 = self.register_and_login(email='grocery_create_list_user_3')
        with self.client:
            data = self.gh.create_grocery_list(auth_token=user_auth_1['auth_token'],
                                               payload=grocery_list_payload)
            self.assertTrue(data['data']['name'] == grocery_list_payload['name'],
                            msg='Received: {}'.format(data['data']['name']))
            self.assertTrue(data['data']['description'] == grocery_list_payload['description'],
                            msg='Received: {}'.format(data['data']['name']))
            self.assertTrue(isinstance(data['data']['id'], str),
                            msg=f"type for id is:: {type(data['data']['id'])}")
            # self.assertTrue(data['data']['total_items'] == 0)

            # share with email and list id
            share_payload = {'email': user_auth_2['user_data']['email'],
                             'grocery_list_id': data['data']['id']}
            data = self.gh.share_grocery_list(auth_token=user_auth_1['auth_token'],
                                              payload=share_payload)
            expected_status_msg = 'Grocery List {} was shared with user {}.'.format(share_payload["grocery_list_id"],
                                                                                    share_payload["email"])
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == expected_status_msg)
            self.assertEqual(data['status_code'], 200)

            req_response = self.gh.get_all_grocery_lists(auth_token=user_auth_2['auth_token'])
            gls = GroceriesList.query.filter_by(name=grocery_list_payload['name']).first()
            self.assertTrue(req_response['data'][0]['name'] == grocery_list_payload['name'])
            self.assertTrue(req_response['data'][0]['description'] == grocery_list_payload['description'])
            # self.assertTrue(req_response['data'][0]['total_items'] == 0)
            self.assertTrue(req_response['data'][0]['id'] == str(gls.id))

    def test_user_cannot_view_groceries_lists_that_are_not_shared_with_him_or_owned(self):
        """
        Test that user cannot view lists that are not owned or shared with him.
        """
        grocery_list_payload = {'name': 'Cannot Share Grocery List',
                                'description': 'Cannot Share Grocery List of 2020'}
        user_auth_4 = self.register_and_login(email='grocery_create_list_user_4')
        user_auth_5 = self.register_and_login(email='grocery_create_list_user_5')
        user_auth_6 = self.register_and_login(email='grocery_create_list_user_6')
        with self.client:
            data = self.gh.create_grocery_list(auth_token=user_auth_4['auth_token'],
                                               payload=grocery_list_payload)
            self.assertTrue(data['data']['name'] == grocery_list_payload['name'],
                            msg='Received: {}'.format(data['data']['name']))

            # share with email and list id
            sharing_payload = {'email': user_auth_5['user_data']['email'],
                               'grocery_list_id': data['data']['id']}
            print(f'share_cannot_share_with_view:: {data}')
            data = self.gh.share_grocery_list(payload=sharing_payload, auth_token=user_auth_5['auth_token'])

            expected_status_msg = 'Grocery List {} was shared with user {}.'.format(sharing_payload["grocery_list_id"],
                                                                                    sharing_payload["email"])
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == expected_status_msg)
            self.assertEqual(data['status_code'], 200)

            req_response = self.gh.get_all_grocery_lists(auth_token=user_auth_5['auth_token'])
            gls = GroceriesList.query.filter_by(name=grocery_list_payload['name']).first()
            self.assertTrue(req_response['data'][0]['name'] == grocery_list_payload['name'])
            self.assertTrue(req_response['data'][0]['description'] == grocery_list_payload['description'])
            # self.assertTrue(req_response['data'][0]['total_items'] == 0)
            self.assertTrue(req_response['data'][0]['id'] == str(gls.id))

            req_response = self.gh.get_all_grocery_lists(auth_token=user_auth_6['auth_token'])
            self.assertTrue(req_response['status'] == 'success')
            self.assertTrue(req_response['data'] == [])
            self.assertEqual(req_response['status_code'], 200)

    def test_user_can_remove_another_user_from_a_shared_grocery_list(self):
        """
        Test that a user can remove another user from a shared grocery list.
        """
        grocery_list_payload = {'name': 'Grocery List 4',
                                'description': 'Grocery List of 2020'}
        user_auth_7 = self.register_and_login(email='grocery_create_list_user_7')
        user_auth_8 = self.register_and_login(email='grocery_create_list_user_8')
        user_auth_9 = self.register_and_login(email='grocery_create_list_user_9')
        with self.client:
            data = self.gh.create_grocery_list(auth_token=user_auth_7['auth_token'],
                                               payload=grocery_list_payload)
            self.assertTrue(data['data']['name'] == grocery_list_payload['name'],
                            msg='Received: {}'.format(data['data']['name']))

            # share with email and list id
            sharing_payload = {'email': user_auth_8['user_data']['email'],
                               'grocery_list_id': data['data']['id']}
            data = self.gh.share_grocery_list(auth_token=user_auth_7['auth_token'],
                                              payload=sharing_payload)

            expected_status_msg = 'Grocery List {} was shared with user {}.'.format(sharing_payload["grocery_list_id"],
                                                                                    sharing_payload["email"])
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == expected_status_msg)
            self.assertEqual(data['status_code'], 200)

            req_response = self.gh.get_all_grocery_lists(auth_token=user_auth_8['auth_token'])
            gls = GroceriesList.query.filter_by(name=grocery_list_payload['name']).first()
            self.assertTrue(req_response['data'][0]['name'] == grocery_list_payload['name'])
            self.assertTrue(req_response['data'][0]['description'] == grocery_list_payload['description'])
            # self.assertTrue(req_response['data'][0]['total_items'] == 0)
            self.assertTrue(req_response['data'][0]['id'] == str(gls.id))

            req_response = self.gh.get_all_grocery_lists(auth_token=user_auth_9['auth_token'])
            self.assertTrue(req_response['status'] == 'success')
            self.assertTrue(req_response['data'] == [])
            self.assertEqual(req_response['status_code'], 200)

            data = self.gh.remove_share_grocery_list(auth_token=user_auth_7['auth_token'],
                                                     payload=sharing_payload)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Grocery List with id: {} was un-shared.'.format(gls.id))

            req_response = self.gh.get_all_grocery_lists(auth_token=user_auth_8['auth_token'])
            self.assertTrue(req_response['status'] == 'success')
            self.assertTrue(req_response['data'] == [])
            self.assertEqual(req_response['status_code'], 200)

    def test_can_add_item_to_grocery_list(self):
        """
        Test that can add item to a grocery list.
        """
        grocery_list_payload = {'name': 'Grocery List With Added Item',
                                'description': 'Item in List of 2020 Added List'}
        user_auth = self.register_and_login(email='grocery_add_item_to_grocery_list')
        with self.client:
            data = self.gh.create_grocery_list(auth_token=user_auth['auth_token'],
                                               payload=grocery_list_payload)
            self.assertTrue(data['status'] == 'success',
                            msg=f'Failed to create groceries list. \nReceived data is:\n {data}')
            item_payload = {'name': 'New Item',
                            'description': 'New Item Description'}
            item_added_response = self.gh.add_item_to_list(auth_token=user_auth['auth_token'],
                                                           gls_id=data['data']['id'],
                                                           payload=item_payload)
            self.assertTrue(item_added_response['status'] == 'success')

    def test_can_delete_a_grocery_list_item(self):
        """
        Test that can delete a grocery list item.
        """
        user_auth = self.register_and_login(email='grocery_delete_list_item_user')
        self.add_groceries_lists(grocery_list_name='grocery_delete_list_user', user_data=user_auth)
        with self.client:
            gls_id = self.gls[3]['id']
            item_payload = {'name': 'New Item To Delete',
                            'description': 'New Item To Delete Description'}
            item_added_response = self.gh.add_item_to_list(auth_token=user_auth['auth_token'],
                                                           gls_id=gls_id,
                                                           payload=item_payload)
            print(f'{item_added_response=}')
            self.assertTrue(item_added_response['status'] == 'success')
            delete_payload = {'item_id': item_added_response['data']['id']}
            item_deleted_response = self.gh.delete_item_from_grocery_list(auth_token=user_auth['auth_token'],
                                                                          gls_id=gls_id,
                                                                          payload=delete_payload)
            assert_msg = 'Grocery List Item with id: {} was deleted.'
            self.assertTrue(item_deleted_response['message'] == assert_msg.format(delete_payload['item_id']),
                            msg=item_deleted_response['message'])


if __name__ == '__main__':
    unittest.main()
