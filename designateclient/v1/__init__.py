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
from designateclient import utils


class Client(object):
    """Client for the Designate v1 API"""

    def __init__(self, endpoint=None, username=None, user_id=None,
                 user_domain_id=None, user_domain_name=None, password=None,
                 tenant_name=None, tenant_id=None, domain_name=None,
                 domain_id=None, project_name=None,
                 project_id=None, project_domain_name=None,
                 project_domain_id=None, auth_url=None, token=None,
                 endpoint_type=None, region_name=None, service_type=None,
                 insecure=False):
        """
        :param endpoint: Endpoint URL
        :param token: A token instead of username / password
        :param insecure: Allow "insecure" HTTPS requests
        """
        if not endpoint or not token:
            ksclient = utils.get_ksclient(
                username=username, user_id=user_id,
                user_domain_id=user_domain_id,
                user_domain_name=user_domain_name, password=password,
                tenant_id=tenant_id, tenant_name=tenant_name,
                project_id=project_id, project_name=project_name,
                project_domain_id=project_domain_id,
                project_domain_name=project_domain_name,
                auth_url=auth_url,
                token=token,
                insecure=insecure)
            ksclient.authenticate()

            token = token or ksclient.auth_token

            filters = {
                'region_name': region_name,
                'service_type': service_type,
                'endpoint_type': endpoint_type,
            }
            endpoint = endpoint or self._get_endpoint(ksclient, **filters)

        self.endpoint = endpoint.rstrip('/')

        # NOTE(kiall): As we're in the Version 1 client, we ensure we're
        #              pointing at the version 1 API.
        if not self.endpoint.endswith('v1'):
            self.endpoint = "%s/v1" % self.endpoint

        self.insecure = insecure

        headers = {'Content-Type': 'application/json'}

        if token is not None:
            headers['X-Auth-Token'] = token

        self.requests = requests.Session()
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

        if self.insecure is True:
            kw['verify'] = False

        # Trigger the request
        response = func(*args, **kw)

        # Decode is response, if possible
        try:
            response_payload = response.json()
        except ValueError:
            response_payload = {}

        if response.status_code == 400:
            raise exceptions.BadRequest(**response_payload)
        elif response.status_code in (401, 403):
            raise exceptions.Forbidden(**response_payload)
        elif response.status_code == 404:
            raise exceptions.NotFound(**response_payload)
        elif response.status_code == 409:
            raise exceptions.Conflict(**response_payload)
        elif response.status_code >= 500:
            raise exceptions.Unknown(**response_payload)
        else:
            return response

    def _get_endpoint(self, client, **kwargs):
        """Get an endpoint using the provided keystone client."""
        if kwargs.get('region_name'):
            return client.service_catalog.url_for(
                service_type=kwargs.get('service_type') or 'dns',
                attr='region',
                filter_value=kwargs.get('region_name'),
                endpoint_type=kwargs.get('endpoint_type') or 'publicURL')
        return client.service_catalog.url_for(
            service_type=kwargs.get('service_type') or 'dns',
            endpoint_type=kwargs.get('endpoint_type') or 'publicURL')

    def get(self, path, **kw):
        return self.wrap_api_call(self.requests.get, path, **kw)

    def post(self, path, **kw):
        return self.wrap_api_call(self.requests.post, path, **kw)

    def put(self, path, **kw):
        return self.wrap_api_call(self.requests.put, path, **kw)

    def delete(self, path, **kw):
        return self.wrap_api_call(self.requests.delete, path, **kw)
