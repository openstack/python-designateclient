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

from designateclient.cli import base
from designateclient.v2.tlds import Tld

LOG = logging.getLogger(__name__)


class ListTldsCommand(base.ListCommand):
    """List Tlds"""

    columns = ['id', 'name']

    def execute(self, parsed_args):
        return self.client.tlds.list()


class GetTldCommand(base.GetCommand):
    """Get Tld"""

    def get_parser(self, prog_name):
        parser = super(GetTldCommand, self).get_parser(prog_name)

        parser.add_argument('id', help="Tld ID")

        return parser

    def execute(self, parsed_args):
        return self.client.tlds.get(parsed_args.id)


class CreateTldCommand(base.CreateCommand):
    """Create Tld"""

    def get_parser(self, prog_name):
        parser = super(CreateTldCommand, self).get_parser(prog_name)

        parser.add_argument('--name', help="Tld Name", required=True)

        return parser

    def execute(self, parsed_args):
        tld = Tld(
            name=parsed_args.name,
        )

        return self.client.tlds.create(tld)


class UpdateTldCommand(base.UpdateCommand):
    """Update Tld"""

    def get_parser(self, prog_name):
        parser = super(UpdateTldCommand, self).get_parser(prog_name)

        parser.add_argument('id', help="Tld ID")
        parser.add_argument('--name', help="Tld Name")
        return parser

    def execute(self, parsed_args):

        tld = {}
        args = vars(parsed_args)
        cols = ['id','name','description']
        for col in cols:
            if col in args:
                tld[col] = args[col]
        
        tld = {'tld': tld}

        return self.client.tlds.update(tld)


class DeleteTldCommand(base.DeleteCommand):
    """Delete Tld"""

    def get_parser(self, prog_name):
        parser = super(DeleteTldCommand, self).get_parser(prog_name)

        parser.add_argument('id', help="Tld ID")

        return parser

    def execute(self, parsed_args):
        return self.client.tlds.delete(parsed_args.id)
