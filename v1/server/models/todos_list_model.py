#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'

from uuid import uuid4
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import UniqueConstraint

from flask_jwt_auth.v1.server import db_sql
from flask_jwt_auth.v1.server.models import BaseModel

# Base = declarative_base()
# todo_list_users = db_sql.Table('todo_list_users', Base.metadata,
#                                db_sql.Column('todo_list_id', UUID(as_uuid=True),
#                                              db_sql.ForeignKey('todo_lists.id'),
#                                              primary_key=True),
#                                db_sql.Column('user_id', UUID(as_uuid=True),
#                                              db_sql.ForeignKey('users.id'),
#                                              primary_key=True))


class TodoListUsers(BaseModel):
    __tablename__ = 'todo_list_users'
    __table_args__ = (UniqueConstraint('todo_list_id', 'user_id', name='todo_list_users_idx'),)

    todo_list_id = db_sql.Column(db_sql.ForeignKey('todo_lists.id'),
                                 default=uuid4, nullable=False, unique=False,
                                 primary_key=True)
    user_id = db_sql.Column(db_sql.ForeignKey('users.id', ondelete='CASCADE'),
                            default=uuid4, nullable=False, unique=False,
                            primary_key=True)
    owner = db_sql.Column(db_sql.Boolean, default=True, nullable=False, unique=False)

    def __init__(self, user_id, todo_list_id, owner=True):
        super().__init__()
        self.user_id = user_id
        self.todo_list_id = todo_list_id
        self.owner = owner


class TodoList(BaseModel):
    """
    Todos List Model for storing TODOs list.
    """
    __tablename__ = 'todo_lists'

    name = db_sql.Column(db_sql.String(255), unique=True, nullable=False)
    description = db_sql.Column(db_sql.String(255), unique=False, nullable=True)
    items = db_sql.relationship('TodoItem', backref='todo_lists', lazy=True)
    # users = db_sql.relationship('User', back_populates='todo_lists')
    users = db_sql.relationship('User', back_populates='todo_list_users')

    def __init__(self, name, description):
        super().__init__()
        self.name = name
        self.description = description

        self.total_items = 0

        if self.auto_save:
            self.save()


class TodoListItem(BaseModel):
    """
    Todos List Item Model for storing TODOs list items.
    """
    __tablename__ = 'todo_items'
    FK_USERS = db_sql.ForeignKey('users.id')
    FK_TODOS_LIST = db_sql.ForeignKey('todo_lists.id')

    name = db_sql.Column(db_sql.String(255), unique=True, nullable=False)
    description = db_sql.Column(db_sql.String(255), unique=False, nullable=True)

    user_id = db_sql.Column(FK_USERS, default=uuid4, nullable=False, unique=False,
                            primary_key=False)
    todo_list_id = db_sql.Column(FK_TODOS_LIST, default=uuid4, nullable=False,
                                 unique=False, primary_key=False)
    todo_list = db_sql.relationship('TodoList', back_populates='todo_items')

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
