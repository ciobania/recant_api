#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
# from sqlalchemy.orm import relationship

from flask_jwt_auth.v1.server import db_sql
from flask_jwt_auth.v1.server.models import BaseModel


class ProductCategory(BaseModel):
    """
    Product Category Model for storing shopping products details.
    """
    __tablename__ = 'product_categories'
    __optional_params = ('description',)

    name = db_sql.Column(db_sql.String(255), unique=True, nullable=False)
    description = db_sql.Column(db_sql.String(255), unique=False, nullable=True)
    parent_id = db_sql.Column(db_sql.ForeignKey('product_categories.id'), unique=False, nullable=True)

    def __init__(self, name, parent_id=None, **kwargs):
        super().__init__()
        self.name = name
        self.parent_id = parent_id

        for received_param in set(kwargs).intersection(set(self.__optional_params)):
            setattr(self, received_param, kwargs.get(received_param))

        if self.auto_save:
            self.save()
