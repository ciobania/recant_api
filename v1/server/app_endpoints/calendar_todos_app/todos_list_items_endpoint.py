#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'

from flask import make_response, jsonify, g, request
from flask.views import MethodView

from flask_jwt_auth.v1.server.auth.auth_helpers import login_required
from flask_jwt_auth.v1.server.models import TodoItem, TodoList


class TodoItemEndpoint(MethodView):
    @login_required
    def get(self, todo_list_id, item_id):
        """
        Scaffolding for GET HTTP request: /todos/<uuid:todo_list_id>/item/<uuid:item_id>
        :return: JSON API response
        """
        if todo_list_id and item_id:
            list_item = TodoItem.query.\
                filter_by(todo_list_id=todo_list_id).\
                filter_by(id=item_id)
            return make_response(jsonify(list_item[0]))
        elif (not todo_list_id and item_id) or \
                (todo_list_id and not item_id) or \
                (not todo_list_id and not item_id):
            response_object = {'status': 'fail',
                               'message': 'todo_list_id or item_id are missing or empty.'}
            return make_response(jsonify(response_object)), 404

    @login_required
    def post(self, todo_list_id):
        """
        Scaffolding for GET HTTP request: /todos/<uuid:todo_list_id>/item
        :return: JSON API response
        """
        request_payload = request.get_json()
        if todo_list_id:
            todo_list = TodoList.query.filter_by(id=todo_list_id)[0]
            if not todo_list:
                response_object = {'status': 'fail',
                                   'message': 'Resource not found.'}
                return make_response(jsonify(response_object)), 404
            list_item = {'name': request_payload.get('name'),
                         'description': request_payload.get('description')}
            new_list_item = TodoItem(**list_item, todo_list_id=todo_list_id, user=g.user).as_dict()
            response_object = {'status': 'success',
                               'data': new_list_item}
            return make_response(jsonify(response_object)), 200

    @login_required
    def delete(self, todo_list_id, item_id):
        """
        Scaffolding for DELETE HTTP request: /todos/<uuid:todo_list_id>/item/<uuid:item_id>
        :return: JSON API response
        """
        if todo_list_id and item_id:
            list_item = TodoItem.query.\
                filter_by(todo_list_id=todo_list_id).\
                filter_by(id=item_id)
            if not list_item:
                response_object = {'status': 'fail',
                                   'message': 'Resource not found.'}
                return make_response(jsonify(response_object)), 404
            else:
                response_object = {'status': 'success',
                                   'message': 'Todo List Item with id: {} was deleted.'.format(item_id)}
                list_item.delete()
                list_item.session.commit()
            return make_response(jsonify(response_object))
        elif (not todo_list_id and item_id) or \
                (todo_list_id and not item_id) or \
                (not todo_list_id and not item_id):
            response_object = {'status': 'fail',
                               'message': 'todo_list_id or item_id are missing or empty.'}
            return make_response(jsonify(response_object)), 404
