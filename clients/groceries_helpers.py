#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from flask_jwt_auth.clients.request_helpers import RequestHelpers


class GroceriesHelpers:
    def __init__(self, client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = client
        self.rh = RequestHelpers(self.client)

    def share_grocery_list(self, payload, auth_token):
        data = self.rh.request('/api/groceries/share',
                               'post',
                               auth_token=auth_token,
                               payload=payload)

        return data

    def remove_share_grocery_list(self, payload, auth_token):
        data = self.rh.request('/api/groceries/share',
                               'delete',
                               auth_token=auth_token,
                               payload=payload)

        return data

    def get_all_grocery_lists(self, auth_token):
        data = self.rh.request('/api/groceries',
                               'get',
                               auth_token=auth_token)
        return data

    def create_grocery_list(self, payload, auth_token):
        data = self.rh.request('/api/groceries',
                               'post',
                               auth_token=auth_token,
                               payload=payload)
        print(f'created_grocery_list:: {data}')

        return data

    def update_grocery_list(self, payload, auth_token, gls_id):
        data = self.rh.request('/api/groceries/{}'.format(gls_id),
                               'post',
                               auth_token=auth_token,
                               payload=payload)

        return data

    def delete_grocery_list(self, auth_token, gls_id):
        data = self.rh.request('/api/groceries/{}'.format(gls_id),
                               'delete',
                               auth_token=auth_token)

        return data

    def add_item_to_list(self, auth_token, gls_id, payload):
        data = self.rh.request('/api/groceries/{}/item'.format(gls_id),
                               'post',
                               auth_token=auth_token,
                               payload=payload)

        return data

    def delete_item_from_grocery_list(self, auth_token, gls_id, payload):
        data = self.rh.request('/api/groceries/{}/item/{}'.format(gls_id, payload['item_id']),
                               'delete',
                               auth_token=auth_token,
                               payload=payload)
        return data
