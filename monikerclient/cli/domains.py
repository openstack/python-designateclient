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
from monikerclient.cli import base
from monikerclient.v1.domains import Domain

LOG = logging.getLogger(__name__)


class ListDomainsCommand(base.ListCommand):
    """ List Domains """

    def execute(self, parsed_args):
        return self.client.domains.list()


class GetDomainCommand(base.GetCommand):
    """ Get Domain """

    def get_parser(self, prog_name):
        parser = super(GetDomainCommand, self).get_parser(prog_name)

        parser.add_argument('--domain-id', help="Domain ID", required=True)

        return parser

    def execute(self, parsed_args):
        return self.client.domains.get(parsed_args.domain_id)


class CreateDomainCommand(base.CreateCommand):
    """ Create Domain """

    def get_parser(self, prog_name):
        parser = super(CreateDomainCommand, self).get_parser(prog_name)

        parser.add_argument('--domain-name', help="Domain Name", required=True)
        parser.add_argument('--domain-email', help="Domain Email",
                            required=True)

        return parser

    def execute(self, parsed_args):
        domain = Domain(
            name=parsed_args.domain_name,
            email=parsed_args.domain_email
        )

        return self.client.domains.create(domain)


class UpdateDomainCommand(base.UpdateCommand):
    """ Update Domain """

    def get_parser(self, prog_name):
        parser = super(UpdateDomainCommand, self).get_parser(prog_name)

        parser.add_argument('--domain-id', help="Domain ID", required=True)
        parser.add_argument('--domain-name', help="Domain Name")
        parser.add_argument('--domain-email', help="Domain Email")

        return parser

    def execute(self, parsed_args):
        # TODO: API needs updating.. this get is silly
        domain = self.client.domains.get(parsed_args.domain_id)

        # TODO: How do we tell if an arg was supplied or intentionally set to
        #       None?

        return self.client.domains.update(domain)


class DeleteDomainCommand(base.DeleteCommand):
    """ Delete Domain """

    def get_parser(self, prog_name):
        parser = super(DeleteDomainCommand, self).get_parser(prog_name)

        parser.add_argument('--domain-id', help="Domain ID")

        return parser

    def execute(self, parsed_args):
        return self.client.domains.delete(parsed_args.domain_id)
