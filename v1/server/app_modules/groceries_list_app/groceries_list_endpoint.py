#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from datetime import datetime
from uuid import NAMESPACE_DNS, uuid5

from flask import make_response, jsonify, g, request
from flask.views import MethodView

from flask_jwt_auth.v1.server.auth.auth_helpers import login_required

inventory = {
    1: {'name': "Grocery List 1",
        'description': 'A first grocery list 1.',
        'id': uuid5(NAMESPACE_DNS, "Grocery List 1"),
        'total_items': 10,
        'created_at': datetime.now(),
        'created_by': 10003}
}


class GroceriesListEndpoint(MethodView):
    @login_required
    def get(self, grocery_list_id):
        """
        Scaffolding for GET HTTP request: /groceries/
        :return: JSON API response
        """
        if grocery_list_id:
            grocery_list_obj = tuple(item for item in inventory.values()
                                     if item['id'] == uuid5(NAMESPACE_DNS, "Grocery List 1"))
            return make_response(jsonify(grocery_list_obj[0]))
        else:
            return make_response(jsonify(tuple(inventory.values()))), 200

    @login_required
    def post(self, grocery_list_id):
        """
        Scaffolding for GET HTTP request: /groceries/<name>
        :return: JSON API response
        """
        request_payload = request.get_json()
        if not grocery_list_id:
            add_grocery_list = {'name': request_payload.get('name'),
                                'description': request_payload.get('description'),
                                'id': uuid5(NAMESPACE_DNS, request_payload.get('name')),
                                'total_items': 0,
                                'created_at': datetime.now(),
                                'created_by': g.user.id}
            inventory[len(inventory)] = dict(add_grocery_list)

            return make_response(jsonify(add_grocery_list)), 200
        elif grocery_list_id:
            request_payload = request.get_json()
            response_object = {'name': request_payload.get('name'),
                               'description': request_payload.get('description'),
                               'id': grocery_list_id,
                               'total_items': 14,
                               'created_at': datetime.now(),
                               'created_by': g.user.id}
            # if request_payload.keys()
            # validate payload for POST request
            return make_response(jsonify(response_object))

    @login_required
    def delete(self, grocery_list_id):
        """
        Scaffolding for DELETE HTTP request: /groceries/<uuid:grocery_list_id>
        :return: JSON API response
        """

        if grocery_list_id:
            response_object = {'status': 'success',
                               'message': 'Grocery List with id: {} was deleted.'.format(grocery_list_id)}
            return make_response(jsonify(response_object))
