# Copyright 2012 Managed I.T.
#
# Author: Kiall Mac Innes <kiall@managedit.ie>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import requests
from stevedore import extension
from designateclient import exceptions
from designateclient.auth import KeystoneAuth


class Client(object):
    """ Client for the Designate v1 API """

    def __init__(self, endpoint=None, auth_url=None, username=None,
                 password=None, tenant_id=None, tenant_name=None, token=None,
                 region_name=None, service_type='dns',
                 endpoint_type='publicURL', sudo_tenant_id=None):
        """
        :param endpoint: Endpoint URL
        :param auth_url: Keystone auth_url
        :param username: The username to auth with
        :param password: The password to auth with
        :param tenant_id: The tenant ID
        :param tenant_name: The tenant name
        :param token: A token instead of username / password
        :param region_name: The region name
        :param endpoint_type: The endpoint type (publicURL for example)
        """
        if auth_url:
            auth = KeystoneAuth(auth_url, username, password, tenant_id,
                                tenant_name, token, service_type,
                                endpoint_type, sudo_tenant_id)
            if endpoint:
                self.endpoint = endpoint
            else:
                self.endpoint = auth.get_url()
        elif endpoint:
            auth = None
            self.endpoint = endpoint
        else:
            raise ValueError('Either an endpoint or auth_url must be supplied')

        headers = {'Content-Type': 'application/json'}
        self.requests = requests.Session()
        self.requests.auth = auth
        self.requests.headers.update(headers)

        def _load_controller(ext):
            controller = ext.plugin(client=self)
            setattr(self, ext.name, controller)

        # Load all controllers
        mgr = extension.ExtensionManager('designateclient.v1.controllers')
        mgr.map(_load_controller)

    def wrap_api_call(self, func, *args, **kw):
        """
        Wrap a self.<rest function> with exception handling

        :param func: The function to wrap
        """
        # Prepend the endpoint URI
        args = list(args)
        args[0] = '%s/%s' % (self.endpoint, args[0])

        # Trigger the request
        response = func(*args, **kw)

        if response.status_code == 400:
            raise exceptions.BadRequest(**response.json())
        elif response.status_code in (401, 403):
            raise exceptions.Forbidden(**response.json())
        elif response.status_code == 404:
            raise exceptions.NotFound(**response.json())
        elif response.status_code == 409:
            raise exceptions.Conflict(**response.json())
        elif response.status_code == 500:
            raise exceptions.Unknown(**response.json())
        else:
            return response

    def get(self, path, **kw):
        return self.wrap_api_call(self.requests.get, path, **kw)

    def post(self, path, **kw):
        return self.wrap_api_call(self.requests.post, path, **kw)

    def put(self, path, **kw):
        return self.wrap_api_call(self.requests.put, path, **kw)

    def delete(self, path, **kw):
        return self.wrap_api_call(self.requests.delete, path, **kw)
