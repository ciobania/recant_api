#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from datetime import datetime
from uuid import NAMESPACE_DNS, uuid5

from flask import make_response, jsonify
from flask.views import MethodView


class GroceriesListEndpoint(MethodView):
    def get(self):
        name = 'Grocery List 1'
        get_groceries_list = {'name': name,
                              'id': uuid5(NAMESPACE_DNS, name),
                              'total_items': 10,
                              'created_at': datetime.now(),
                              'created_by': 'me as string for now'}
        return make_response(jsonify(get_groceries_list)), 200
