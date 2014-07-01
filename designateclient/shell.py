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

        parser.add_argument('--os-endpoint',
                            default=os.environ.get('OS_DNS_ENDPOINT'),
                            help="Defaults to env[OS_DNS_ENDPOINT]")

        parser.add_argument('--os-auth-url',
                            default=os.environ.get('OS_AUTH_URL'),
                            help="Defaults to env[OS_AUTH_URL]")

        parser.add_argument('--os-username',
                            default=os.environ.get('OS_USERNAME'),
                            help="Defaults to env[OS_USERNAME]")

        parser.add_argument('--os-password',
                            default=os.environ.get('OS_PASSWORD'),
                            help="Defaults to env[OS_PASSWORD]")

        parser.add_argument('--os-tenant-id',
                            default=os.environ.get('OS_TENANT_ID'),
                            help="Defaults to env[OS_TENANT_ID]")

        parser.add_argument('--os-tenant-name',
                            default=os.environ.get('OS_TENANT_NAME'),
                            help="Defaults to env[OS_TENANT_NAME]")

        parser.add_argument('--os-token',
                            default=os.environ.get('OS_SERVICE_TOKEN'),
                            help="Defaults to env[OS_SERVICE_TOKEN]")

        parser.add_argument('--os-service-type',
                            default=os.environ.get('OS_DNS_SERVICE_TYPE',
                                                   'dns'),
                            help=("Defaults to env[OS_DNS_SERVICE_TYPE], or "
                                  "'dns'"))

        parser.add_argument('--os-region-name',
                            default=os.environ.get('OS_REGION_NAME'),
                            help="Defaults to env[OS_REGION_NAME]")

        parser.add_argument('--sudo-tenant-id',
                            default=os.environ.get('DESIGNATE_SUDO_TENANT_ID'),
                            help="Defaults to env[DESIGNATE_SUDO_TENANT_ID]")

        parser.add_argument('--insecure', action='store_true',
                            help="Explicitly allow 'insecure' SSL requests")

        return parser
