#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from flask import request, jsonify, make_response
from flask.views import MethodView

from flask_jwt_auth.project.server import db_sql
from flask_jwt_auth.project.server.models import User


class RegisterEndpoint(MethodView):
    """
    User Registration Endpoint API.
    """
    def post(self):
        """
        Scaffolding for POST HTTP method
        :return: JSON API response
        """
        post_payload = request.get_json()
        email = post_payload.get('email')
        password = post_payload.get('password')
        user = User.query.filter_by(email=email).first()
        if not user:
            try:
                user = User(email=email, password=password)
                db_sql.session.add(user)
                db_sql.session.commit()
                auth_token = user.encode_auth_token(user_id=user.id)
                response_object = {'status': 'success',
                                   'message': 'Successfully registered.',
                                   'auth_token': auth_token.decode()}
                return make_response(jsonify(response_object)), 201
            except Exception as _:
                response_object = {'status': 'fail',
                                   'message': 'Some error occurred. Please try again later.'}
                return make_response(jsonify(response_object)), 401
        else:
            response_object = {'status': 'fail',
                               'message': 'User already exists. Please Log In.'}
            return make_response(jsonify(response_object)), 202
