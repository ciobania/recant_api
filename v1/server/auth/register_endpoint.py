#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from flask import request, jsonify, make_response
from flask.views import MethodView
from psycopg2.errors import UniqueViolation

from flask_jwt_auth.v1.server.models import User, Role


class RegisterEndpoint(MethodView):
    """
    User Registration Endpoint API.
    """
    def post(self):
        """
        Scaffolding for POST HTTP method: /auth/register
        :return: JSON API response
        """
        post_payload = request.get_json()
        email = post_payload.get('email')
        password = post_payload.get('password')
        user = User.query.filter_by(email=email).first()
        if not user:
            try:
                role_name = 'normal_user'
                role = Role.query.filter_by(name=role_name).first()
                if not role:
                    role = Role(role_name)

                user = User(email=email, password=password, roles=[role])
                auth_token = user.encode_auth_token(user_id=user.id)
                response_object = {'status': 'success',
                                   'message': 'Successfully registered.',
                                   'auth_token': auth_token.decode()}
                return make_response(jsonify(response_object)), 201
            except Exception as _:
                err_msg = 'Error occurred: {}. Please try again later.'
                response_object = {'status': 'fail',
                                   'message': err_msg.format(_)}
                return make_response(jsonify(response_object)), 401
        else:
            response_object = {'status': 'fail',
                               'message': 'User already exists. Please Log In.'}
            return make_response(jsonify(response_object)), 202
