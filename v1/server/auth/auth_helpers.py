#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
import functools

from flask import request, jsonify, make_response, g

from flask_jwt_auth.v1.server.models import User


def login_required(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                _, auth_token = auth_header.split()
            except ValueError as _:
                response_object = {'status': 'fail',
                                   'message': 'Authorization Bearer token is missing or malformed.'}
                return make_response(jsonify(response_object)), 400
        else:
            auth_token = ''
        if auth_token:
            response = User.decode_auth_token(auth_token=auth_token)
            if not isinstance(response, str):
                user = User.query.filter_by(id=response).first()
                if user:
                    g.user = user
                    return method(self, *args, **kwargs)
                else:
                    response_object = {'status': 'fail',
                                       'message': 'User not found.'}
                    return make_response(jsonify(response_object)), 400
            response_object = {'status': 'fail',
                               'message': response}
            return make_response(jsonify(response_object)), 401
        else:
            response_object = {'status': 'fail',
                               'message': 'Provide a valid auth token.'}
            return make_response(jsonify(response_object)), 403
    return wrapper
