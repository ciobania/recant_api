#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'

from flask import Blueprint

from flask_jwt_auth.project.server.auth.login_endpoint import LoginEndpoint
from flask_jwt_auth.project.server.auth.logout_endpoint import LogoutEndpoint
from flask_jwt_auth.project.server.auth.register_endpoint import RegisterEndpoint
from flask_jwt_auth.project.server.auth.user_auth_status_endpoint import UserAuthStatusEndpoint

auth_bp = Blueprint('auth', __name__)

# define auth API resources
registration_view = RegisterEndpoint.as_view('register_api')
login_view = LoginEndpoint.as_view('login_api')
auth_status_view = UserAuthStatusEndpoint.as_view('auth_status_api')
logout_view = LogoutEndpoint.as_view('logout_api')

auth_bp.add_url_rule('/auth/register',
                     view_func=registration_view,
                     methods=['POST'])
auth_bp.add_url_rule('/auth/login',
                     view_func=login_view,
                     methods=['POST'])
auth_bp.add_url_rule('/auth/status',
                     view_func=auth_status_view,
                     methods=['GET'])
auth_bp.add_url_rule('/auth/logout',
                     view_func=logout_view,
                     methods=['POST'])
