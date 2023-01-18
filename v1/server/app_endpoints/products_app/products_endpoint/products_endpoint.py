#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from flask import make_response, jsonify, g, request
from flask.views import MethodView

from flask_jwt_auth.v1.server.auth.auth_helpers import login_required
from flask_jwt_auth.v1.server.models import Product


class ProductsEndpoint(MethodView):
    # @login_required
    def get(self, product_id):
        """
        Scaffolding for GET HTTP request: /products/
        :return: JSON API response
        """

        if product_id:
            try:
                product = Product.query.filter_by(id=product_id).first()
                if not product:
                    response_object = {'status': 'fail',
                                       'message': 'Resource not found.'}
                    return make_response(jsonify(response_object)), 404
                response_object = {'status': 'success',
                                   'data': product.as_dict()}
                return make_response(jsonify(response_object)), 200
            except Exception as _:
                err_msg = 'Error occurred: {}. Please try again later.'
                response_object = {'status': 'fail',
                                   'message': err_msg.format(_)}
                return make_response(jsonify(response_object)), 401
        else:
            products_list = Product.query.filter().order_by(Product.created_at).all()
            todo_ls = [item.as_dict() for item in products_list if products_list]
            response_object = {'status': 'success',
                               'data': todo_ls}
            return make_response(jsonify(response_object)), 200

    # @login_required
    def post(self, product_id):
        """
        Scaffolding for POST HTTP request: /products/<uuid:product_id>
        :return: JSON API response
        """
        request_payload = request.get_json()
        name = request_payload.get('name')
        description = request_payload.get('description')
        brand_name = request_payload.get('brand_name')
        gtin = request_payload.get('gtin')
        status = request_payload.get('status')
        price = request_payload.get('price')
        unit_price = request_payload.get('unit_price')
        unit_of_measure = request_payload.get('unit_of_measure')
        category_id = request_payload.get('category_id')

        if not product_id:
            add_product = {'name': name,
                           'description': description,
                           'brand_name': brand_name,
                           'gtin': gtin,
                           'status': status,
                           'price': price,
                           'unit_price': unit_price,
                           'unit_of_measure': unit_of_measure,
                           'category_id': category_id}
            print(f'saving:: {add_product=}')

            new_product = Product(**add_product).as_dict()

            response_object = {'status': 'success',
                               'data': new_product}
            return make_response(jsonify(response_object)), 200
        elif product_id:
            product = Product.query.filter_by(id=product_id).first()
            if not product:
                response_object = {'status': 'fail',
                                   'message': 'Resource not found.'}
                return make_response(jsonify(response_object)), 404
            request_payload = request.get_json()
            product.name = request_payload.get('name')
            product.description = request_payload.get('description')
            product.save()

            # if request_payload.keys()
            # validate payload for POST request
            return make_response(jsonify(product.as_dict())), 200

    # @login_required
    def delete(self, product_id):
        """
        Scaffolding for DELETE HTTP request: /products/<uuid:product_id>
        :return: JSON API response
        """

        if product_id:
            response_object = {'status': 'success',
                               'message': 'Product with id: {} was deleted.'.format(product_id)}
            product = Product.query.filter(user_id=g.user.id, product_id=product_id)
            if not product:
                response_object = {'status': 'fail',
                                   'message': 'Resource not found.'}
                return make_response(jsonify(response_object)), 404
            else:
                product.delete(synchronize_session='fetch')
                product.session.commit()
            return make_response(jsonify(response_object))
