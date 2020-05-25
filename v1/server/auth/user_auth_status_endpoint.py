#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from flask import jsonify, make_response, g
from flask.views import MethodView

from flask_jwt_auth.v1.server.auth.auth_helpers import login_required


class UserAuthStatusEndpoint(MethodView):
    """
    User Auth Status API Endpoint
    """
    @login_required
    def get(self):
        """
        Scaffolding for GET HTTP method: /auth/status
        :return: JSON API response
        """
        response_object = {'status': 'success',
                           'data': {'user_id': g.user.id,
                                    'email': g.user.email,
                                    'admin': g.user.admin,
                                    'registered_on': g.user.registered_on}}
        return make_response(jsonify(response_object)), 200
