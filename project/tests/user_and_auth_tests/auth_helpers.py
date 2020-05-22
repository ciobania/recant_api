#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
import json


class AuthHelpers:
    def __init__(self, client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = client

    def register_user(self, user_payload):
        # response = self.client.post('/auth/register',
        #                             data=json.dumps(user_payload),
        #                             content_type='application/json')
        # data = json.loads(response.data.decode())
        # data['content_type'] = response.content_type
        # data['status_code'] = response.status_code
        data = self._request('/auth/register', 'post', user_payload=user_payload)

        return data

    def login_user(self, user_payload):
        # response = self.client.post('/auth/login',
        #                             data=json.dumps(user_payload),
        #                             content_type='application/json')
        # data = json.loads(response.data.decode())
        # data['content_type'] = response.content_type
        # data['status_code'] = response.status_code
        data = self._request('/auth/login', 'post', user_payload=user_payload)

        return data

    def logout_user(self, auth_token):
        # headers = {'Authorization': 'Bearer {}'.format(auth_token)}
        # response = self.client.post('/auth/logout',
        #                             headers=headers)
        # data = json.loads(response.data.decode())
        # data['content_type'] = response.content_type
        # data['status_code'] = response.status_code
        data = self._request('/auth/logout', 'post', auth_token=auth_token)

        return data

    def auth_status(self, auth_token):
        # headers = {'Authorization': 'Bearer {}'.format(auth_token)}
        # response = self.client.get('/auth/status',
        #                            headers=headers)
        # data = json.loads(response.data.decode())
        # data['content_type'] = response.content_type
        # data['status_code'] = response.status_code
        data = self._request('/auth/status', 'get', auth_token=auth_token)

        return data

    def _request(self, url, r_method, **kwargs):
        headers = None
        data = None
        if 'auth_token' in kwargs:
            headers = {'Authorization': 'Bearer {}'.format(kwargs['auth_token'])}
        elif 'user_payload' in kwargs:
            data = json.dumps(kwargs['user_payload'])
        if headers:
            response = getattr(self.client, r_method)(url, headers=headers)
        if data:
            response = getattr(self.client, r_method)(url, data=data, content_type='application/json')

        data = json.loads(response.data.decode())
        data['content_type'] = response.content_type
        data['status_code'] = response.status_code

        return data
