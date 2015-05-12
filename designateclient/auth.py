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

from keystoneclient.v2_0.client import Client
from requests.auth import AuthBase


class KeystoneAuth(AuthBase):
    def __init__(self, auth_url, username=None, password=None, tenant_id=None,
                 tenant_name=None, token=None, service_type=None,
                 endpoint_type=None, region_name=None, sudo_tenant_id=None):
        self.auth_url = str(auth_url).rstrip('/')
        self.username = username
        self.password = password
        self.tenant_id = tenant_id
        self.tenant_name = tenant_name
        self.token = token
        self.sudo_tenant_id = sudo_tenant_id

        if (not username and not password) and not token:
            raise ValueError('A username and password, or token is required')

        if not service_type or not endpoint_type:
            raise ValueError("Need service_type and/or endpoint_type")

        self.service_type = service_type
        self.endpoint_type = endpoint_type
        self.region_name = region_name

        self.refresh_auth()

    def __call__(self, request):
        if not self.token:
            self.refresh_auth()

        request.headers['X-Auth-Token'] = self.token

        if self.sudo_tenant_id:
            request.headers['X-Designate-Sudo-Tenant-ID'] = self.sudo_tenant_id

        return request

    def get_ksclient(self):
        insecure = urlparse(self.auth_url).scheme != 'https'

        return Client(username=self.username,
                      password=self.password,
                      tenant_id=self.tenant_id,
                      tenant_name=self.tenant_name,
                      auth_url=self.auth_url,
                      insecure=insecure)

    def get_endpoints(self, service_type=None, endpoint_type=None,
                      region_name=None):
        return self.service_catalog.get_endpoints(
            service_type=service_type,
            endpoint_type=endpoint_type,
            region_name=region_name)

    def get_url(self, service_type=None, endpoint_type=None, region_name=None):
        service_type = service_type or self.service_type
        endpoint_type = endpoint_type or self.endpoint_type
        region_name = region_name or self.region_name

        endpoints = self.get_endpoints(service_type, endpoint_type,
                                       region_name)

        url = endpoints[service_type][0][endpoint_type]

        # NOTE(kiall): The Version 1 API is the only API that has ever included
        #              the version number in the endpoint. Thus, it's safe to
        #              simply remove it if present.
        url = url.rstrip('/')
        if url.endswith('/v1'):
            url = url[:-3]
        return url

    def refresh_auth(self):
        ks = self.get_ksclient()
        self.token = ks.auth_token
        self.service_catalog = ks.service_catalog
