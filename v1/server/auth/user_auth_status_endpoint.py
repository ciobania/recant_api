#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from flask import request, jsonify, make_response
from flask.views import MethodView

from flask_jwt_auth.v1.server.models import User


class UserAuthStatusEndpoint(MethodView):
    """
    User Auth Status API Endpoint
    """
    def get(self):
        """
        Scaffolding for POST HTTP method
        :return: JSON API response
        """
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                _, auth_token = auth_header.split()
            except ValueError as _:
                response_object = {'status': 'fail',
                                   'message': 'Bearer token is malformed.'}
                return make_response(jsonify(response_object)), 400
        else:
            auth_token = ''
        if auth_token:
            response = User.decode_auth_token(auth_token=auth_token)
            if not isinstance(response, str):
                user = User.query.filter_by(id=response).first()
                response_object = {'status': 'success',
                                   'data': {'user_id': user.id,
                                            'email': user.email,
                                            'admin': user.admin,
                                            'registered_on': user.registered_on}}
                return make_response(jsonify(response_object)), 200
            response_object = {'status': 'fail',
                               'message': response}
            return make_response(jsonify(response_object)), 401
        else:
            response_object = {'status': 'fail',
                               'message': 'Provide a valid auth token.'}
            return make_response(jsonify(response_object)), 403
