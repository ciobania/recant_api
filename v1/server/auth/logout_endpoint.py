#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from flask import request, jsonify, make_response
from flask.views import MethodView

from flask_jwt_auth.v1.server.models import User, BlacklistToken


class LogoutEndpoint(MethodView):
    """
    Logout API Endpoint.
    """
    def post(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(' ')[1]
        else:
            auth_token = ''
        if auth_token:
            response = User.decode_auth_token(auth_token=auth_token)
            if not isinstance(response, str):
                blacklist_token = BlacklistToken(token=auth_token)
                try:
                    blacklist_token.save(force_insert=True)
                    response_object = {'status': 'success',
                                       'message': 'Successfully logged out.'}
                    return make_response(jsonify(response_object)), 200
                except Exception as _:
                    response_object = {'status': 'fail',
                                       'message': _}
                    return make_response(jsonify(response_object)), 401
            else:
                response_object = {'status': 'fail',
                                   'message': response}
                return make_response(jsonify(response_object)), 400
        else:
            response_object = {'status': 'fail',
                               'message': 'Provide a valid auth token.'}
            return make_response(jsonify(response_object)), 403
