#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from flask import make_response, jsonify, g, request
from flask.views import MethodView

from flask_jwt_auth.v1.server.auth.auth_helpers import login_required
from flask_jwt_auth.v1.server.models import Product
from flask_jwt_auth.v1.server.models import ProductCategory


class ProductCategoriesEndpoint(MethodView):
    # @login_required
    def get(self, category_id):
        """
        Scaffolding for GET HTTP request: /product_categories/
        :return: JSON API response
        """
        if category_id:
            try:
                category = ProductCategory.query.filter_by(id=category_id).first()
                if not category:
                    response_object = {'status': 'fail',
                                       'message': 'Resource not found.'}
                    return make_response(jsonify(response_object)), 404
                response_object = {'status': 'success',
                                   'data': category.as_dict()}
                return make_response(jsonify(response_object)), 200
            except Exception as _:
                err_msg = 'Error occurred: {}. Please try again later.'
                response_object = {'status': 'fail',
                                   'message': err_msg.format(_)}
                return make_response(jsonify(response_object)), 401
        else:
            product_categories_list = ProductCategory.query.filter().order_by(ProductCategory.created_at).all()
            product_categories_ls = [item.as_dict() for item in product_categories_list]
            response_object = {'status': 'success',
                               'data': product_categories_ls}
            return make_response(jsonify(response_object)), 200

    # @login_required
    def post(self, category_id):
        """
        Scaffolding for POST HTTP request: /product_categories/<uuid:category_id>
        :return: JSON API response
        """
        request_payload = request.get_json()
        name = request_payload.get('name')
        description = request_payload.get('description')
        parent_id = request_payload.get('parent_id')

        if not category_id:
            add_category = {'name': name,
                            'description': description,
                            'parent_id': parent_id}
            print(f'saving:: {add_category}')

            new_category = ProductCategory(**add_category).as_dict()

            response_object = {'status': 'success',
                               'data': new_category}
            return make_response(jsonify(response_object)), 200
        elif category_id:
            category = ProductCategory.query.filter_by(id=category_id).first()
            if not category:
                response_object = {'status': 'fail',
                                   'message': 'Resource not found.'}
                return make_response(jsonify(response_object)), 404
            request_payload = request.get_json()
            category.name = request_payload.get('name')
            category.description = request_payload.get('description')
            category.save()

            # if request_payload.keys()
            # validate payload for POST request
            return make_response(jsonify(category.as_dict())), 200

    # @login_required
    def delete(self, category_id):
        """
        Scaffolding for DELETE HTTP request: /product_categories/<uuid:category_id>
        :return: JSON API response
        """

        if category_id:
            response_object = {'status': 'success',
                               'message': 'Product with id: {} was deleted.'.format(category_id)}
            category = ProductCategory.query.filter(user_id=g.user.id, category_id=category_id)
            if not category:
                response_object = {'status': 'fail',
                                   'message': 'Resource not found.'}
                return make_response(jsonify(response_object)), 404
            else:
                category.delete(synchronize_session='fetch')
                category.session.commit()
            return make_response(jsonify(response_object))
