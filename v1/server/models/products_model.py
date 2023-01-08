#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from flask_jwt_auth.v1.server import db_sql
from flask_jwt_auth.v1.server.models import BaseModel


class Product(BaseModel):
    """
    Product Model for storing shopping products details.
    """
    __tablename__ = 'products'
    __optional_params = ('description', 'status')

    name = db_sql.Column(db_sql.String(255), unique=True, nullable=False)
    description = db_sql.Column(db_sql.String(255), unique=False, nullable=True)
    brand_name = db_sql.Column(db_sql.String(255), unique=False, nullable=False)
    gtin = db_sql.Column(db_sql.String(255), unique=False, nullable=False)
    status = db_sql.Column(db_sql.String(100), unique=False, nullable=False)
    price = db_sql.Column(db_sql.Integer, unique=False, nullable=False)
    unit_price = db_sql.Column(db_sql.Integer, unique=False, nullable=False)
    unit_of_measure = db_sql.Column(db_sql.String(12), unique=False, nullable=False)
    # "shelfId": "b;QmFieSU3Q0JhYnklMjAmJTIwVG9kZGxlciUyME1pbGslN0NGaXJzdCUyMEJhYnklMjBNaWxrJTIwRnJvbSUyMEJpcnRoJTdDRmly
    # c3QlMjBCYWJ5JTIwTWlsayUyMGZyb20lMjBCaXJ0aA=="
    # category_id = db_sql.Column()

    def __init__(self, name, brand_name, gtin, price, unit_price, unit_of_measure, **kwargs):
        super().__init__()
        self.name = name
        self.brand_name = brand_name
        self.gtin = gtin
        self.price = price
        self.unit_price = unit_price
        self.unit_of_measure = unit_of_measure

        for received_param in set(kwargs).intersection(set(self.__optional_params)):
            setattr(self, received_param, kwargs.get(received_param))

        if self.auto_save:
            self.save()
