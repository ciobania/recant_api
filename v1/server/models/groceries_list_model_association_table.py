#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from uuid import uuid4
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from flask_jwt_auth.v1.server import db_sql
from flask_jwt_auth.v1.server.models import BaseModel


class SharedGroceriesList(BaseModel):
    __tablename__ = 'shared_groceries_lists'
    FK_USERS = db_sql.ForeignKey('users.id')
    FK_GROCERIES_LIST = db_sql.ForeignKey('groceries_list.id', ondelete='CASCADE')

    user_id = db_sql.Column(UUID(as_uuid=True), FK_USERS, default=uuid4, nullable=False, unique=False, primary_key=True)
    grocery_list_id = db_sql.Column(UUID(as_uuid=True), FK_GROCERIES_LIST, default=uuid4, nullable=False,
                                    unique=False, primary_key=True)
    owner = db_sql.Column(db_sql.Boolean, default=uuid4, nullable=False, unique=False)
    UniqueConstraint('user_id', 'grocery_list_id', name='shared_groceries_list_idx')


class GroceriesList(BaseModel):
    """
    Groceries List Model for storing shopping groceries list.
    """
    __tablename__ = 'groceries_list'

    name = db_sql.Column(db_sql.String(255), unique=True, nullable=False)
    description = db_sql.Column(db_sql.String(255), unique=False, nullable=True)

    users = db_sql.relationship('User', secondary=shared_groceries_lists,
                                backref=db_sql.backref('users', lazy='joined'))

    def __init__(self, name, description, user):
        super().__init__()
        self.name = name
        self.description = description

        self.users.append(user)
        self.created_by = user.id
        self.total_items = 0

        if self.auto_save:
            self.save()

    def as_dict(self):
        response_object = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        if hasattr(self, 'created_by'):
            response_object['created_by'] = str(self.created_by)

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

    user_id = db_sql.Column(UUID(as_uuid=True), FK_USERS, default=uuid4, nullable=False, unique=False,
                            primary_key=False)
    grocery_list_id = db_sql.Column(UUID(as_uuid=True), FK_GROCERIES_LIST, default=uuid4, nullable=False,
                                    unique=False, primary_key=False)

    def __init__(self, name, description, user):
        super().__init__()
        self.name = name
        self.description = description

        self.created_by = user.id
        self.quantity = 0

        if self.auto_save:
            self.save()

    def as_dict(self):
        response_object = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        if hasattr(self, 'created_by'):
            response_object['created_by'] = str(self.created_by)

        return response_object
