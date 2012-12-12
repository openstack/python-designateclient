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
from urlparse import urlparse
from monikerclient import exceptions
from monikerclient.auth import KeystoneAuth
from monikerclient.v1 import domains
from monikerclient.v1 import records
from monikerclient.v1 import servers


class Client(object):
    """ Client for the Moniker v1 API """

    def __init__(self, endpoint=None, auth_url=None, username=None,
                 password=None, tenant_id=None, tenant_name=None, token=None,
                 region_name=None, endpoint_type='publicURL'):
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
                                tenant_name, token, 'dns', endpoint_type)
            endpoint = auth.get_url()
        elif endpoint:
            auth = None
        else:
            raise ValueError('Either an endpoint or auth_url must be supplied')

        headers = {'Content-Type': 'application/json'}

        def _ensure_url_hook(args):
            url_ = urlparse(args['url'])
            if not url_.scheme:
                args['url'] = endpoint + url_.path

        hooks = {'args': _ensure_url_hook}

        self.requests = requests.session(
            auth=auth,
            headers=headers,
            hooks=hooks)

        self.domains = domains.DomainsController(client=self)
        self.records = records.RecordsController(client=self)
        self.servers = servers.ServersController(client=self)

    def wrap_api_call(self, func, *args, **kw):
        """
        Wrap a self.<rest function> with exception handling

        :param func: The function to wrap
        """
        response = func(*args, **kw)

        if response.status_code == 400:
            raise exceptions.BadRequest(response.json['errors'])
        elif response.status_code in (401, 403):
            raise exceptions.Forbidden()
        elif response.status_code == 404:
            raise exceptions.NotFound()
        elif response.status_code == 409:
            raise exceptions.Conflict()
        elif response.status_code == 500:
            raise exceptions.Unknown()
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
