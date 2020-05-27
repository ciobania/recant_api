#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from uuid import uuid4

from flask_security import RoleMixin

from flask_jwt_auth.v1.server import db_sql
from flask_jwt_auth.v1.server.models import BaseModel

user_roles = db_sql.Table('user_roles', BaseModel.metadata,
                          db_sql.Column('user_id', db_sql.ForeignKey('users.id'), default=uuid4,
                                        nullable=False, unique=True),
                          db_sql.Column('role_id', db_sql.ForeignKey('roles.id'),  default=uuid4,
                                        nullable=False, unique=True))


class Role(BaseModel, RoleMixin):
    """
    Role Model for storing role related details.
    """
    __tablename__ = 'roles'

    name = db_sql.Column(db_sql.String(64), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name
