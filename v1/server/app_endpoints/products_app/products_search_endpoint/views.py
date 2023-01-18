#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'

from flask import Blueprint

from flask_jwt_auth.v1.server.app_endpoints.products_app.products_search_endpoint import ProductsSearchEndpoint

products_search_bp = Blueprint('products_search', __name__)

# define auth API resources
products_search_view = ProductsSearchEndpoint.as_view('products_search_api')

products_search_bp.add_url_rule('/api/products/search',
                                # defaults={'product_name': None,
                                #           'category_name': None,
                                #           'search_term': None},
                                view_func=products_search_view,
                                methods=['GET', 'POST'])
