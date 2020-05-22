#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from flask import request, jsonify, make_response
from flask.views import MethodView

from flask_jwt_auth.project.server import bcrypt
from flask_jwt_auth.project.server.models import User


class LoginEndpoint(MethodView):
    """
    User Login Endpoint API.
    """
    def post(self):
        """
        Scaffolding for POST HTTP method
        :return: JSON API response
        """
        post_payload = request.get_json()
        try:
            user = User.query.filter_by(email=post_payload.get('email')).first()
            if user and bcrypt.check_password_hash(user.password, post_payload.get('password')):
                auth_token = user.encode_auth_token(user_id=user.id)
                if auth_token:
                    response_object = {'status': 'success',
                                       'message': 'Successfully logged in.',
                                       'auth_token': auth_token.decode()}
                    return make_response(jsonify(response_object)), 200
            elif user and not bcrypt.check_password_hash(user.password, post_payload.get('password')):
                response_object = {'status': 'fail',
                                   'message': 'Incorrect password.'}
                return make_response(jsonify(response_object)), 400
            else:
                response_object = {'status': 'fail',
                                   'message': 'User does not exist.'}
                return make_response(jsonify(response_object)), 404
        except Exception as _:
            response_object = {'status': 'fail',
                               'message': 'Try again.'}
            return make_response(jsonify(response_object)), 500
