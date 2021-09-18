#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from flask import make_response, jsonify, g, request
from flask.views import MethodView

from flask_jwt_auth.v1.server.auth.auth_helpers import login_required
from flask_jwt_auth.v1.server.models import GroceriesList


class GroceriesListEndpoint(MethodView):
    @login_required
    def get(self, grocery_list_id):
        """
        Scaffolding for GET HTTP request: /groceries/
        :return: JSON API response
        """

        if grocery_list_id:
            try:
                grocery_list = GroceriesList.query.filter_by(id=grocery_list_id).first()
                response_object = {'status': 'success',
                                   'data': grocery_list}
                return make_response(jsonify(response_object)), 200
            except Exception as _:
                err_msg = 'Error occurred: {}. Please try again later.'
                response_object = {'status': 'fail',
                                   'message': err_msg.format(_)}
                return make_response(jsonify(response_object)), 401
        else:
            filter_gl = GroceriesList.shared_with.any(user_id=g.user.id)
            groceries_list = GroceriesList.query.filter(filter_gl).order_by(GroceriesList.created_at).all()
            gls = [item.as_dict() for item in groceries_list if groceries_list]
            response_object = {'status': 'success',
                               'data': gls}
            return make_response(jsonify(response_object)), 200

    @login_required
    def post(self, grocery_list_id):
        """
        Scaffolding for POST HTTP request: /groceries/<uuid:grocery_list_id>
        :return: JSON API response
        """
        request_payload = request.get_json()
        if not grocery_list_id:
            add_grocery_list = {'name': request_payload.get('name'),
                                'description': request_payload.get('description')}
            new_grocery_list = GroceriesList(**add_grocery_list, user=g.user).as_dict()

            response_object = {'status': 'success',
                               'data': new_grocery_list}
            return make_response(jsonify(response_object)), 200
        elif grocery_list_id:
            grocery_list = GroceriesList.query.filter_by(id=grocery_list_id).first()
            if not grocery_list:
                response_object = {'status': 'fail',
                                   'message': 'Resource not found.'}
                return make_response(jsonify(response_object)), 404
            request_payload = request.get_json()
            grocery_list.name = request_payload.get('name')
            grocery_list.description = request_payload.get('description')
            grocery_list.save()

            # if request_payload.keys()
            # validate payload for POST request
            return make_response(jsonify(grocery_list.as_dict())), 200

    @login_required
    def delete(self, grocery_list_id):
        """
        Scaffolding for DELETE HTTP request: /groceries/<uuid:grocery_list_id>
        :return: JSON API response
        """

        if grocery_list_id:
            response_object = {'status': 'success',
                               'message': 'Grocery List with id: {} was deleted.'.format(grocery_list_id)}
            filter_gl = GroceriesList.shared_with.any(user_id=g.user.id, grocery_list_id=grocery_list_id, owner=True)
            grocery_list = GroceriesList.query.filter(filter_gl)
            if not grocery_list:
                response_object = {'status': 'fail',
                                   'message': 'Resource not found.'}
                return make_response(jsonify(response_object)), 404
            else:
                grocery_list.delete(synchronize_session='fetch')
                grocery_list.session.commit()
            return make_response(jsonify(response_object))
