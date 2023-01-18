#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from datetime import datetime
from uuid import NAMESPACE_DNS, uuid5

from flask import make_response, jsonify, g, request
from flask.views import MethodView

from flask_jwt_auth.v1.server import User
from flask_jwt_auth.v1.server.auth.auth_helpers import login_required
from flask_jwt_auth.v1.server.models import GroceriesList
from flask_jwt_auth.v1.server.models.groceries_list_model import SharedGroceriesList


class GroceryListShareEndpoint(MethodView):
    @login_required
    def post(self):
        """
        Scaffolding for POST HTTP request: /groceries/share
        :return: JSON API response
        """
        request_payload = request.get_json()
        print(f'{request_payload=}')
        email = request_payload.get('email')
        grocery_list_id = request_payload.get('grocery_list_id')
        print(f'filtering by grocery_list_id:: {grocery_list_id}')
        user_to_share_with = User.query.filter_by(email=email).first()
        if not user_to_share_with:
            # TODO: throw error
            pass
        else:
            grocery_list = GroceriesList.query.filter_by(id=grocery_list_id).first()
            sgl = SharedGroceriesList(user_id=user_to_share_with.id, grocery_list_id=grocery_list.id)
            sgl.save()
            response_message = f'Grocery List {grocery_list_id} was shared with user {email}.'
            response_object = {'status': 'success',
                               'message': response_message}
            return make_response(jsonify(response_object)), 200

    @login_required
    def delete(self):
        """
        Scaffolding for DELETE HTTP request: /groceries/share/<uuid:user_id>
        :return: JSON API response
        """
        request_payload = request.get_json()
        grocery_list_id = request_payload.get('grocery_list_id')
        email = request_payload.get('email')

        user = SharedGroceriesList.user.has(email=email)
        filter_gl = GroceriesList.shared_with.any(grocery_list_id=grocery_list_id)
        grocery_list = GroceriesList.query.filter(filter_gl, user)
        grocery_list.delete(synchronize_session=False)
        response_object = {'status': 'success',
                           'message': 'Grocery List with id: {} was un-shared.'.format(grocery_list_id)}
        return make_response(jsonify(response_object))
