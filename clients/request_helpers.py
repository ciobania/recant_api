#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
import json


class RequestHelpers:
    def __init__(self, client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = client

    def request(self, url, r_method, **kwargs):
        headers = None
        data = None
        response = None
        if 'auth_token' in kwargs:
            headers = {'Authorization': 'Bearer {}'.format(kwargs['auth_token'])}
        if 'payload' in kwargs:
            data = json.dumps(kwargs['payload'])
        if headers and data:
            response = getattr(self.client, r_method)(url,
                                                      headers=headers,
                                                      data=data,
                                                      content_type='application/json')
        elif headers:
            response = getattr(self.client, r_method)(url, headers=headers)
        elif data:
            response = getattr(self.client, r_method)(url,
                                                      data=data,
                                                      content_type='application/json')

        response_type = ("<class 'flask_testing.utils._make_test_response.<locals>.TestResponse'>", )
        response_type = ("<class 'werkzeug.test.WrapperTestResponse'>", )
        if response and repr(type(response)) in response_type:
            data = {'status': 'success'}
            try:
                json_response = json.loads(response.data.decode())
                if isinstance(json_response, (tuple, list)):
                    data['data'] = json_response
                else:
                    data.update(json_response)
            except json.decoder.JSONDecodeError as _:
                data = {'status': 'fail', 'message': _, 'text': response.data}

            data['content_type'] = response.content_type
            data['status_code'] = response.status_code

            return data
        else:
            err_msg = 'Response type is: {}.\nExpected type is {}.\n'
            # raise NotImplementedError(err_msg.format(type(response), response_type))
