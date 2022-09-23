#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'

from uuid import uuid4


from flask_jwt_auth.v1.server import db_sql
from flask_jwt_auth.v1.server.models import BaseModel


class TodosList(BaseModel):
    """
    Todos List Model for storing shopping groceries list.
    """
    __tablename__ = 'todos_list'

    name = db_sql.Column(db_sql.String(255), unique=True, nullable=False)
    description = db_sql.Column(db_sql.String(255), unique=False, nullable=True)

    # users = db_sql.relationship('User')

    # gls = db_sql.relationship('users', back_populates='shared_groceries_lists')
    # gls = db_sql.relationship('GroceriesList', secondary=shared_groceries_lists,
    #                           backref=db_sql.backref('groceries_list', lazy='joined'))
    # owner = association_proxy('shared_groceries_lists', 'owner')

    def __init__(self, name, description):
        super().__init__()
        self.name = name
        self.description = description

        # self.users.append(user)
        self.total_items = 0

        if self.auto_save:
            self.save()


class TodosListItem(BaseModel):
    """
    Todos List Item Model for storing shopping groceries list items.
    """
    __tablename__ = 'todos_list_item'
    FK_USERS = db_sql.ForeignKey('users.id')
    FK_TODOS_LIST = db_sql.ForeignKey('todos_list.id')

    name = db_sql.Column(db_sql.String(255), unique=True, nullable=False)
    description = db_sql.Column(db_sql.String(255), unique=False, nullable=True)

    user_id = db_sql.Column(FK_USERS, default=uuid4, nullable=False, unique=False,
                            primary_key=False)
    todos_list_id = db_sql.Column(FK_TODOS_LIST, default=uuid4, nullable=False,
                                  unique=False, primary_key=False)

    def __init__(self, name, description, todo_list_id, user):
        super().__init__()
        self.name = name
        self.description = description
        self.todo_list_id = todo_list_id
        self.user_id = user.id
        self.created_by = user.id
        self.quantity = 0

        if self.auto_save:
            self.save()
