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
from keystoneclient import adapter
from keystoneclient.auth.identity import generic
from keystoneclient.auth import token_endpoint
from keystoneclient import session as ks_session
from stevedore import extension

from designateclient import exceptions
from designateclient import version


class Client(object):
    """Client for the Designate v1 API"""

    def __init__(self, endpoint=None, username=None, user_id=None,
                 user_domain_id=None, user_domain_name=None, password=None,
                 tenant_name=None, tenant_id=None, domain_name=None,
                 domain_id=None, project_name=None,
                 project_id=None, project_domain_name=None,
                 project_domain_id=None, auth_url=None, token=None,
                 endpoint_type='publicURL', region_name=None,
                 service_type='dns', insecure=False, verify=None, session=None,
                 auth=None):
        """
        :param endpoint: Endpoint URL
        :param token: A token instead of username / password
        :param insecure: Allow "insecure" HTTPS requests
        """
        # Backwards compat to preserve the functionality of insecure.
        if verify is None and insecure:
            verify = False
        else:
            verify = True

        # Compatibility code to mimic the old behaviour of the client
        if session is None:
            session = ks_session.Session(verify=verify)

            auth_args = {
                'auth_url': auth_url,
                'domain_id': domain_id,
                'domain_name': domain_name,
                'project_id': project_id,
                'project_name': project_name,
                'project_domain_name': project_domain_name,
                'project_domain_id': project_domain_id,
                'tenant_id': tenant_id,
                'tenant_name': tenant_name,
            }

            if token:
                # To mimic typical v1 behaviour I copied this
                endpoint = endpoint.rstrip('/')
                if not endpoint.endswith('v1'):
                    endpoint = "%s/v1" % endpoint
                session.auth = token_endpoint.Token(endpoint, token)
            else:
                password_args = {
                    'username': username,
                    'user_id': user_id,
                    'user_domain_id': user_domain_id,
                    'user_domain_name': user_domain_name,
                    'password': password
                }
                auth_args.update(password_args)
                session.auth = generic.Password(**auth_args)

        # Since we have to behave nicely like a legacy client/bindings we use
        # an adapter around the session to not modify it's state.
        interface = endpoint_type.rstrip('URL')

        self.session = adapter.Adapter(
            session,
            auth=auth,
            endpoint_override=endpoint,
            region_name=region_name,
            service_type=service_type,
            interface=interface,
            user_agent='python-designateclient-%s' % version.version_info,
            version='1'
        )

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
        kw['raise_exc'] = False
        kw.setdefault('headers', {})
        kw['headers'].setdefault('Content-Type', 'application/json')

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

    def get(self, path, **kw):
        return self.wrap_api_call(self.session.get, path, **kw)

    def post(self, path, **kw):
        return self.wrap_api_call(self.session.post, path, **kw)

    def put(self, path, **kw):
        return self.wrap_api_call(self.session.put, path, **kw)

    def delete(self, path, **kw):
        return self.wrap_api_call(self.session.delete, path, **kw)
