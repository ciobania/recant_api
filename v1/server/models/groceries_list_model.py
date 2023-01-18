#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'

from uuid import uuid4

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import backref

from flask_jwt_auth.v1.server import db_sql
from flask_jwt_auth.v1.server.models import BaseModel


class SharedGroceriesList(BaseModel):
    """
    Shared Groceries List Model for storing shared lists of groceries with various users.
    """
    __tablename__ = 'shared_groceries_lists'
    __table_args__ = (UniqueConstraint('user_id', 'grocery_list_id', name='shared_groceries_list_idx'),)

    user_id = db_sql.Column(db_sql.ForeignKey('users.id'), default=uuid4, nullable=False, unique=False)
    user = db_sql.relationship('User', backref=backref('shared_groceries_lists', viewonly=True), foreign_keys=[user_id])
    grocery_list_id = db_sql.Column(db_sql.ForeignKey('groceries_list.id', ondelete='CASCADE'), default=uuid4,
                                    nullable=False, unique=False)
    shared_with = db_sql.relationship('GroceriesList', backref=backref('shared_with', viewonly=True),
                                      foreign_keys=[grocery_list_id])

    def __init__(self, user_id, grocery_list_id):
        super().__init__()
        self.user_id = user_id
        self.grocery_list_id = grocery_list_id


class GroceriesList(BaseModel):
    """
    Groceries List Model for storing shopping groceries list.
    """
    __tablename__ = 'groceries_list'

    name = db_sql.Column(db_sql.String(255), unique=True, nullable=False)
    description = db_sql.Column(db_sql.String(255), unique=False, nullable=True)
    user_id = db_sql.Column(db_sql.ForeignKey('users.id'), default=uuid4, nullable=False, unique=False,
                            primary_key=False)
    users = db_sql.relationship('User', secondary='shared_groceries_lists', viewonly=True,
                                backref=db_sql.backref('shared_groceries_lists.shared_with', lazy='dynamic'))

    def __init__(self, name, description, user_id):
        super().__init__()
        self.name = name
        self.description = description
        self.user_id = user_id
        self.total_items = 0

        if self.auto_save:
            self.save()


class GroceriesListItem(BaseModel):
    """
    Groceries List Item Model for storing shopping groceries list items.
    """
    __tablename__ = 'groceries_list_item'

    name = db_sql.Column(db_sql.String(255), unique=True, nullable=False)
    description = db_sql.Column(db_sql.String(255), unique=False, nullable=True)

    user_id = db_sql.Column(db_sql.ForeignKey('users.id'), default=uuid4, nullable=False,
                            unique=False, primary_key=False)
    user = db_sql.relationship('User', backref=db_sql.backref('groceries_list_items', viewonly=True),
                               foreign_keys=[user_id])
    grocery_list_id = db_sql.Column(db_sql.ForeignKey('groceries_list.id', ondelete='CASCADE'),
                                    default=uuid4, nullable=False, unique=False)
    grocery_list = db_sql.relationship('GroceriesList', backref=db_sql.backref('groceries_list_items',
                                                                               viewonly=True),
                                       foreign_keys=[grocery_list_id])

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
