#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'

from flask import Blueprint

from flask_jwt_auth.v1.server.app_endpoints.products_app.product_categories_endpoint import ProductCategoriesEndpoint

product_categories_bp = Blueprint('product_categories', __name__)

# define auth API resources
product_categories_view = ProductCategoriesEndpoint.as_view('product_categories_api')

product_categories_bp.add_url_rule('/api/product_categories',
                                   defaults={'category_id': None},
                                   view_func=product_categories_view,
                                   methods=['GET', 'POST'])
product_categories_bp.add_url_rule('/api/product_categories/<uuid:category_id>',
                                   view_func=product_categories_view,
                                   methods=['DELETE', 'GET', 'POST'])
