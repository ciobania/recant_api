#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'

from uuid import uuid4, UUID

from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref

from flask_jwt_auth.v1.server import db_sql
from flask_jwt_auth.v1.server.models import BaseModel


class SharedGroceriesList(BaseModel):
    __tablename__ = 'shared_groceries_lists'
    __table_args__ = (UniqueConstraint('user_id', 'grocery_list_id', name='shared_groceries_list_idx'), )

    user_id = db_sql.Column(db_sql.ForeignKey('users.id'), default=uuid4, nullable=False, unique=False)
    grocery_list_id = db_sql.Column(db_sql.ForeignKey('groceries_list.id', ondelete='CASCADE'), default=uuid4,
                                    nullable=False, unique=False)
    owner = db_sql.Column(db_sql.Boolean, default=True, nullable=False, unique=False)
    user = db_sql.relationship('User', backref=backref('user'))
    shared_with = db_sql.relationship('GroceriesList', backref=backref('shared_with'))

    def __init__(self, user_id, grocery_list_id, owner=True):
        super().__init__()
        self.user_id = user_id
        self.grocery_list_id = grocery_list_id
        self.owner = owner


class GroceriesList(BaseModel):
    """
    Groceries List Model for storing shopping groceries list.
    """
    __tablename__ = 'groceries_list'

    name = db_sql.Column(db_sql.String(255), unique=True, nullable=False)
    description = db_sql.Column(db_sql.String(255), unique=False, nullable=True)

    users = db_sql.relationship('User', secondary='shared_groceries_lists',
                                backref=db_sql.backref('shared_groceries_lists', lazy='dynamic'))
    # gls = db_sql.relationship('users', back_populates='shared_groceries_lists')
    # gls = db_sql.relationship('GroceriesList', secondary=shared_groceries_lists,
    #                           backref=db_sql.backref('groceries_list', lazy='joined'))
    # owner = association_proxy('shared_groceries_lists', 'owner')

    def __init__(self, name, description, user):
        super().__init__()
        self.name = name
        self.description = description

        self.users.append(user)
        self.total_items = 0

        if self.auto_save:
            self.save()

    def as_dict(self):
        response_object = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        if hasattr(self, 'created_by'):
            response_object['created_by'] = UUID(str(self.created_by))

        response_object['total_items'] = 0

        return response_object


class GroceriesListItem(BaseModel):
    """
    Groceries List Item Model for storing shopping groceries list items.
    """
    __tablename__ = 'groceries_list_item'
    FK_USERS = db_sql.ForeignKey('users.id')
    FK_GROCERIES_LIST = db_sql.ForeignKey('groceries_list.id')

    name = db_sql.Column(db_sql.String(255), unique=True, nullable=False)
    description = db_sql.Column(db_sql.String(255), unique=False, nullable=True)

    user_id = db_sql.Column(FK_USERS, default=uuid4, nullable=False, unique=False,
                            primary_key=False)
    grocery_list_id = db_sql.Column(FK_GROCERIES_LIST, default=uuid4, nullable=False,
                                    unique=False, primary_key=False)

    def __init__(self, name, description, grocery_list_id, user):
        super().__init__()
        self.name = name
        self.description = description
        self.grocery_list_id = grocery_list_id
        self.user_id = user.id
        self.created_by = user.id
        self.quantity = 0

        if self.auto_save:
            self.save()

    def as_dict(self):
        response_object = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        if hasattr(self, 'created_by'):
            response_object['created_by'] = str(self.created_by)

        return response_object
