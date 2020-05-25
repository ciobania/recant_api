#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from datetime import datetime
from uuid import NAMESPACE_DNS, uuid5

from flask import make_response, jsonify, g
from flask.views import MethodView

from flask_jwt_auth.v1.server.auth.auth_helpers import login_required


class GroceriesListEndpoint(MethodView):
    @login_required
    def get(self):
        """
        Scaffolding for GET HTTP request: /groceries/
        :return: JSON API response
        """
        name = 'Grocery List 1'
        get_groceries_list = {'name': name,
                              'id': uuid5(NAMESPACE_DNS, name),
                              'total_items': 10,
                              'created_at': datetime.now(),
                              'created_by': g.user.id}
        return make_response(jsonify(get_groceries_list)), 200
