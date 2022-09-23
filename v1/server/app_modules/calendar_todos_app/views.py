#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'

from flask import Blueprint

from flask_jwt_auth.v1.server.app_modules.calendar_todos_app.todos_list_endpoint import TodosListEndpoint
from flask_jwt_auth.v1.server.app_modules.calendar_todos_app.todos_list_items_endpoint import TodoListItemEndpoint

todos_calendar_bp = Blueprint('todos_list', __name__)

# define auth API resources
todos_calendar_view = TodosListEndpoint.as_view('todos_calendar_api')
todos_calendar_item_view = TodoListItemEndpoint.as_view('todos_calendar_item_api')
# todos_calendar_share_view = GroceryListShareEndpoint.as_view('todos_calendar_share_api')

todos_calendar_bp.add_url_rule('/api/todos',
                               defaults={'todo_list_id': None},
                               view_func=todos_calendar_view,
                               methods=['GET', 'POST'])
todos_calendar_bp.add_url_rule('/api/todos/<uuid:todo_list_id>',
                               view_func=todos_calendar_view,
                               methods=['DELETE', 'GET', 'POST'])
todos_calendar_bp.add_url_rule('/api/todos/<uuid:todo_list_id>/item',
                               view_func=todos_calendar_item_view,
                               methods=['POST'])
todos_calendar_bp.add_url_rule('/api/todos/<uuid:todo_list_id>/item/<uuid:item_id>',
                               view_func=todos_calendar_item_view,
                               methods=['GET', 'DELETE'])
