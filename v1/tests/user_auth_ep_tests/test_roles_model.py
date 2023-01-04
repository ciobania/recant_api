#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'

import unittest

from flask_jwt_auth.v1.server.models.roles_model import Role
from flask_jwt_auth.v1.tests.base_test_case import BaseTestCase


class TestRolerModel(BaseTestCase):
    session = None
    meta = None

    def setUp(self):
        super(TestRolerModel, self).setUp()

    def tearDown(self):
        super(TestRolerModel, self).tearDown()

    def test_can_create_role_without_description(self):
        """
        Test can create a User Role without a description.
        """
        admin_role = Role('admin_test')
        admin_role.save()


if __name__ == '__main__':
    unittest.main()
