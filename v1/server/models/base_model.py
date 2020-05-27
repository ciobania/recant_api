#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from datetime import datetime
from uuid import uuid4
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID

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
