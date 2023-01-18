#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'

from flask import Blueprint

from flask_jwt_auth.v1.server.app_endpoints.products_app.products_endpoint import ProductsEndpoint

products_bp = Blueprint('products', __name__)

# define auth API resources
products_view = ProductsEndpoint.as_view('products_api')

products_bp.add_url_rule('/api/products',
                         defaults={'product_id': None},
                         view_func=products_view,
                         methods=['GET', 'POST'])
products_bp.add_url_rule('/api/products/<uuid:product_id>',
                         view_func=products_view,
                         methods=['DELETE', 'GET', 'POST'])
