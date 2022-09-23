#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from datetime import datetime
from uuid import uuid4
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError

from flask_jwt_auth.v1.server import db_sql


class BaseModel(db_sql.Model):
    """
    A base model for other database tables to inherit
    """
    __abstract__ = True
    __table_args__ = {'extend_existing': True}

    id = db_sql.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    created_at = db_sql.Column(db_sql.DateTime, nullable=False, server_default=func.now())
    updated_at = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db_sql.Column(db_sql.DateTime, nullable=True, onupdate=datetime.utcnow)

    id._creation_order = 0
    created_at._creation_order = 997
    updated_at._creation_order = 998
    deleted_at._creation_order = 999

    def __init__(self, auto_save=True):
        self.auto_save = auto_save

    def save(self):
        try:
            db_sql.session.add(self)
            db_sql.session.commit()
        except IntegrityError as _:
            db_sql.session.rollback()
            self_params = {param: param_value for param, param_value in self.as_dict().items() if param_value}
            self.__dict__ = dict(db_sql.session.query(self.__table__).filter_by(**self_params).first())

    def delete(self):
        db_sql.session.delete(self)
        db_sql.session.commit()

    def as_dict(self):
        response_object = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        if hasattr(self, 'created_by'):
            response_object['created_by'] = UUID(str(self.created_by))

        for key, value in response_object.items():
            if isinstance(value, UUID):
                response_object[key] = str(value)

        return response_object
