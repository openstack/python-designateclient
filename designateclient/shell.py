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

import logging
import os

from cliff.app import App
from cliff.commandmanager import CommandManager

from designateclient.version import version_info as version


def env(*vars, **kwargs):
    """Search for the first defined of possibly many env vars

    Returns the first environment variable defined in vars, or
    returns the default defined in kwargs.

    """
    for v in vars:
        value = os.environ.get(v)
        if value:
            return value
    return kwargs.get('default', '')


class DesignateShell(App):
    CONSOLE_MESSAGE_FORMAT = '%(levelname)s: %(message)s'
    DEFAULT_VERBOSE_LEVEL = 0

    def __init__(self):
        super(DesignateShell, self).__init__(
            description='Designate Client',
            version=version.version_string(),
            command_manager=CommandManager('designateclient.cli'),
        )

        self.log = logging.getLogger(__name__)

    def build_option_parser(self, description, version):
        parser = super(DesignateShell, self).build_option_parser(
            description, version)

        parser.add_argument('--os-username',
                            default=env('OS_USERNAME'),
                            help='Name used for authentication with the '
                                 'OpenStack Identity service. '
                                 'Defaults to env[OS_USERNAME].')

        parser.add_argument('--os-user-id',
                            default=env('OS_USER_ID'),
                            help='User ID used for authentication with the '
                                 'OpenStack Identity service. '
                                 'Defaults to env[OS_USER_ID].')

        parser.add_argument('--os-user-domain-id',
                            default=env('OS_USER_DOMAIN_ID'),
                            help='Defaults to env[OS_USER_DOMAIN_ID].')

        parser.add_argument('--os-user-domain-name',
                            default=env('OS_USER_DOMAIN_NAME'),
                            help='Defaults to env[OS_USER_DOMAIN_NAME].')

        parser.add_argument('--os-password',
                            default=env('OS_PASSWORD'),
                            help='Password used for authentication with the '
                                 'OpenStack Identity service. '
                                 'Defaults to env[OS_PASSWORD].')

        parser.add_argument('--os-tenant-name',
                            default=env('OS_TENANT_NAME'),
                            help='Tenant to request authorization on. '
                                 'Defaults to env[OS_TENANT_NAME].')

        parser.add_argument('--os-tenant-id',
                            default=env('OS_TENANT_ID'),
                            help='Tenant to request authorization on. '
                                 'Defaults to env[OS_TENANT_ID].')

        parser.add_argument('--os-project-name',
                            default=env('OS_PROJECT_NAME'),
                            help='Project to request authorization on. '
                                 'Defaults to env[OS_PROJECT_NAME].')

        parser.add_argument('--os-domain-name',
                            default=env('OS_DOMAIN_NAME'),
                            help='Project to request authorization on. '
                                 'Defaults to env[OS_DOMAIN_NAME].')

        parser.add_argument('--os-domain-id',
                            default=env('OS_DOMAIN_ID'),
                            help='Defaults to env[OS_DOMAIN_ID].')

        parser.add_argument('--os-project-id',
                            default=env('OS_PROJECT_ID'),
                            help='Project to request authorization on. '
                                 'Defaults to env[OS_PROJECT_ID].')

        parser.add_argument('--os-project-domain-id',
                            default=env('OS_PROJECT_DOMAIN_ID'),
                            help='Defaults to env[OS_PROJECT_DOMAIN_ID].')

        parser.add_argument('--os-project-domain-name',
                            default=env('OS_PROJECT_DOMAIN_NAME'),
                            help='Defaults to env[OS_PROJECT_DOMAIN_NAME].')

        parser.add_argument('--os-auth-url',
                            default=env('OS_AUTH_URL'),
                            help='Specify the Identity endpoint to use for '
                                 'authentication. '
                                 'Defaults to env[OS_AUTH_URL].')

        parser.add_argument('--os-region-name',
                            default=env('OS_REGION_NAME'),
                            help='Specify the region to use. '
                                 'Defaults to env[OS_REGION_NAME].')

        parser.add_argument('--os-token',
                            default=env('OS_SERVICE_TOKEN'),
                            help='Specify an existing token to use instead of '
                                 'retrieving one via authentication (e.g. '
                                 'with username & password). '
                                 'Defaults to env[OS_SERVICE_TOKEN].')

        parser.add_argument('--os-endpoint',
                            default=env('OS_DNS_ENDPOINT',
                                        'OS_SERVICE_ENDPOINT'),
                            help='Specify an endpoint to use instead of '
                                 'retrieving one from the service catalog '
                                 '(via authentication). '
                                 'Defaults to env[OS_DNS_ENDPOINT].')

        parser.add_argument('--os-endpoint-type',
                            default=env('OS_ENDPOINT_TYPE'),
                            help='Defaults to env[OS_ENDPOINT_TYPE].')

        parser.add_argument('--os-service-type',
                            default=env('OS_DNS_SERVICE_TYPE', default='dns'),
                            help=("Defaults to env[OS_DNS_SERVICE_TYPE], or "
                                  "'dns'"))

        parser.add_argument('--insecure', action='store_true',
                            help="Explicitly allow 'insecure' SSL requests")

        return parser
