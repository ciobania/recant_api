#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'

from flask import Blueprint

from flask_jwt_auth.v1.server.app_modules.groceries_list_app.groceries_list_endpoint import GroceriesListEndpoint

groceries_list_bp = Blueprint('groceries_list', __name__)

# define auth API resources
groceries_list_view = GroceriesListEndpoint.as_view('groceries_list_api')

groceries_list_bp.add_url_rule('/api/groceries',
                               defaults={'grocery_list_id': None},
                               view_func=groceries_list_view,
                               methods=['GET', 'POST'])
groceries_list_bp.add_url_rule('/api/groceries/<uuid:grocery_list_id>',
                               view_func=groceries_list_view,
                               methods=['DELETE', 'GET', 'POST'])
