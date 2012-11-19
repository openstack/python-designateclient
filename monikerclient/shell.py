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
import os
from cliff.app import App
from cliff.commandmanager import CommandManager


class MonikerShell(App):
    def __init__(self):
        super(MonikerShell, self).__init__(
            description='Moniker Client',
            version='0.1',
            command_manager=CommandManager('moniker.cli'),
        )

    def build_option_parser(self, description, version, argparse_kwargs=None):
        parser = super(MonikerShell, self).build_option_parser(
            description, version, argparse_kwargs)

        parser.add_argument('--os-endpoint',
                            default=os.environ.get('OS_SERVICE_ENDPOINT'),
                            help="Defaults to env[OS_SERVICE_ENDPOINT]")

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

        parser.add_argument('--os-region-name',
                            default=os.environ.get('OS_REGION_NAME'),
                            help="Defaults to env[OS_REGION_NAME]")

        return parser
