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
from urlparse import urlparse
from requests.auth import AuthBase

from keystoneclient.v2_0.client import Client


class KeystoneAuth(AuthBase):
    def __init__(self, auth_url, username=None, password=None, tenant_id=None,
                 tenant_name=None, token=None, service_type=None,
                 endpoint_type=None):
        self.auth_url = str(auth_url).rstrip('/')
        self.username = username
        self.password = password
        self.tenant_id = tenant_id
        self.tenant_name = tenant_name
        self.token = token

        if (not username and not password) and not token:
            raise ValueError('A username and password, or token is required')

        if not service_type or not endpoint_type:
            raise ValueError("Need service_type and/or endpoint_type")

        self.service_type = service_type
        self.endpoint_type = endpoint_type

        self.refresh_auth()

    def __call__(self, request):
        if not self.token:
            self.refresh_auth()

        request.headers['X-Auth-Token'] = self.token

        return request

    def get_ksclient(self):
        insecure = urlparse(self.auth_url).scheme != 'https'

        return Client(username=self.username,
                      password=self.password,
                      tenant_id=self.tenant_id,
                      tenant_name=self.tenant_name,
                      auth_url=self.auth_url,
                      insecure=insecure)

    def get_endpoints(self, service_type=None, endpoint_type=None):
        return self.service_catalog.get_endpoints(
            service_type=service_type,
            endpoint_type=endpoint_type)

    def get_url(self, service_type=None, endpoint_type=None):
        service_type = service_type or self.service_type
        endpoint_type = endpoint_type or self.endpoint_type
        endpoints = self.get_endpoints(service_type, endpoint_type)

        return endpoints[service_type][0][endpoint_type].rstrip('/')

    def refresh_auth(self):
        ks = self.get_ksclient()
        self.token = ks.auth_token
        self.service_catalog = ks.service_catalog

    def args_hook(self, args):
        url = urlparse(args['url'])

        if str(url.scheme) == '':
            if not self.token:
                self.refresh_token()

            endpoints = self.get_endpoints()

            if url.netloc in endpoints.keys():

                args['url'] = '%s/%s?%s' % (
                    self.get_url(),
                    url.path.lstrip('/'),
                    url.query
                )
