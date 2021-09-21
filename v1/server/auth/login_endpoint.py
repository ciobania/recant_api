#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from flask import request, jsonify, make_response
from flask.views import MethodView

from flask_jwt_auth.v1.server.models import User


class LoginEndpoint(MethodView):
    """
    User Login Endpoint API.
    """
    def post(self):
        """
        Scaffolding for POST HTTP method: /auth/login
        :return: JSON API response
        """
        post_payload = request.get_json()
        print(f'post_payload is:: {post_payload}')
        try:
            user = User.query.filter_by(email=post_payload.get('email')).first()
            print(f'user_type:: {type(user)}')
            # password_is_a_match = user.check_password_hash(post_payload.get('password'))
            password_is_a_match = post_payload.get('password') == user.password
            if user and password_is_a_match:
                auth_token = user.encode_auth_token(user_id=user.id)
                if auth_token:
                    response_object = {'status': 'success',
                                       'message': 'Successfully logged in.',
                                       'auth_token': auth_token}
                    return make_response(jsonify(response_object)), 200
            elif user and not password_is_a_match:
                response_object = {'status': 'fail',
                                   'message': 'Incorrect password.'}
                return make_response(jsonify(response_object)), 400
            else:
                response_object = {'status': 'fail',
                                   'message': 'User does not exist.'}
                return make_response(jsonify(response_object)), 404
        except Exception as _:
            response_object = {'status': 'fail',
                               'message': f'{_}'}
            return make_response(jsonify(response_object)), 500
