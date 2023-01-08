#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from flask import make_response, jsonify, g, request
from flask.views import MethodView

from flask_jwt_auth.v1.server.auth.auth_helpers import login_required
from flask_jwt_auth.v1.server.models import TodoList


class TodosListEndpoint(MethodView):
    @login_required
    def get(self, todo_list_id):
        """
        Scaffolding for GET HTTP request: /todos/
        :return: JSON API response
        """

        if todo_list_id:
            try:
                todo_list = TodoList.query.filter_by(id=todo_list_id).first()
                response_object = {'status': 'success',
                                   'data': todo_list}
                return make_response(jsonify(response_object)), 200
            except Exception as _:
                err_msg = 'Error occurred: {}. Please try again later.'
                response_object = {'status': 'fail',
                                   'message': err_msg.format(_)}
                return make_response(jsonify(response_object)), 401
        else:
            todos_list = TodoList.query.filter().order_by(TodoList.created_at).all()
            todo_ls = [item.as_dict() for item in todos_list if todos_list]
            response_object = {'status': 'success',
                               'data': todo_ls}
            return make_response(jsonify(response_object)), 200

    @login_required
    def post(self, todo_list_id):
        """
        Scaffolding for POST HTTP request: /todos/<uuid:todo_list_id>
        :return: JSON API response
        """
        request_payload = request.get_json()
        if not todo_list_id:
            add_todo_list = {'name': request_payload.get('name'),
                             'description': request_payload.get('description')}
            new_todo_list = TodoList(**add_todo_list).as_dict()

            response_object = {'status': 'success',
                               'data': new_todo_list}
            return make_response(jsonify(response_object)), 200
        elif todo_list_id:
            todo_list = TodoList.query.filter_by(id=todo_list_id).first()
            if not todo_list:
                response_object = {'status': 'fail',
                                   'message': 'Resource not found.'}
                return make_response(jsonify(response_object)), 404
            request_payload = request.get_json()
            todo_list.name = request_payload.get('name')
            todo_list.description = request_payload.get('description')
            todo_list.save()

            # if request_payload.keys()
            # validate payload for POST request
            return make_response(jsonify(todo_list.as_dict())), 200

    @login_required
    def delete(self, todo_list_id):
        """
        Scaffolding for DELETE HTTP request: /todos/<uuid:todo_list_id>
        :return: JSON API response
        """

        if todo_list_id:
            response_object = {'status': 'success',
                               'message': 'ToDo List with id: {} was deleted.'.format(todo_list_id)}
            todo_list = TodoList.query.filter(user_id=g.user.id, todo_list_id=todo_list_id)
            if not todo_list:
                response_object = {'status': 'fail',
                                   'message': 'Resource not found.'}
                return make_response(jsonify(response_object)), 404
            else:
                todo_list.delete(synchronize_session='fetch')
                todo_list.session.commit()
            return make_response(jsonify(response_object))
