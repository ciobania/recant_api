#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'


from sqlalchemy.ext import mutable
import json

from flask_jwt_auth.v1.server import db_sql


class JsonEncodedDict(db_sql.TypeDecorator):
    """
    Enables JSON storage by encoding and decoding on the fly.
    """
    impl = db_sql.Text

    @staticmethod
    def process_bind_param(value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    @staticmethod
    def process_result_value(value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


mutable.MutableDict.associate_with(JsonEncodedDict)
