#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'

from flask_jwt_auth.v1.tests.helpers import RequestHelpers


class AuthHelpers:
    def __init__(self, client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = client
        self.rh = RequestHelpers(self.client)

    def register_user(self, user_payload):
        data = self.rh.request('/auth/register', 'post', user_payload=user_payload)

        return data

    def login_user(self, user_payload):
        data = self.rh.request('/auth/login', 'post', user_payload=user_payload)

        return data

    def logout_user(self, auth_token):
        data = self.rh.request('/auth/logout', 'post', auth_token=auth_token)

        return data

    def auth_status(self, auth_token):
        data = self.rh.request('/auth/status', 'get', auth_token=auth_token)

        return data
