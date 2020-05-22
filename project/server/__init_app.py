#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'

import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app_settings = os.getenv('APP_SETTINGS', 'project.server.config.DevelopmentConfig')
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
