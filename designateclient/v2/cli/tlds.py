# Copyright 2014 Hewlett-Packard Development Company, L.P.
#
# Author: Endre Karlson <endre.karlson@hp.com>
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

from cliff import command
from cliff import lister
from cliff import show
import six

from designateclient import utils
from designateclient.v2.utils import get_all

LOG = logging.getLogger(__name__)


def _format_tld(tld):
    # Remove unneeded fields for display output formatting
    tld.pop('links', None)


class ListTLDsCommand(lister.Lister):
    """List tlds"""

    columns = ['id', 'name', 'description']

    def get_parser(self, prog_name):
        parser = super(ListTLDsCommand, self).get_parser(prog_name)

        parser.add_argument('--name', help="TLD NAME")

        parser.add_argument('--description', help="TLD Description")

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns

        data = get_all(client.tlds.list)

        cols = self.columns
        return cols, (utils.get_item_properties(s, cols) for s in data)


class ShowTLDCommand(show.ShowOne):
    """Show tld details"""

    def get_parser(self, prog_name):
        parser = super(ShowTLDCommand, self).get_parser(prog_name)

        parser.add_argument('id', help="TLD ID")

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns
        data = client.tlds.get(parsed_args.id)
        _format_tld(data)
        return six.moves.zip(*sorted(six.iteritems(data)))


class CreateTLDCommand(show.ShowOne):
    """Create new tld"""

    def get_parser(self, prog_name):
        parser = super(CreateTLDCommand, self).get_parser(prog_name)

        parser.add_argument('--name', help="TLD Name", required=True)
        parser.add_argument('--description', help="Description")

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns
        data = client.tlds.create(parsed_args.name, parsed_args.description)
        _format_tld(data)
        return six.moves.zip(*sorted(six.iteritems(data)))


class SetTLDCommand(show.ShowOne):
    """Set tld properties"""

    def get_parser(self, prog_name):
        parser = super(SetTLDCommand, self).get_parser(prog_name)

        parser.add_argument('id', help="TLD ID")
        parser.add_argument('--name', help="TLD Name")
        description_group = parser.add_mutually_exclusive_group()
        description_group.add_argument('--description', help="Description")
        description_group.add_argument('--no-description', action='store_true')

        return parser

    def take_action(self, parsed_args):
        data = {}

        if parsed_args.name:
            data['name'] = parsed_args.name

        if parsed_args.no_description:
            data['description'] = None
        elif parsed_args.description:
            data['description'] = parsed_args.description

        client = self.app.client_manager.dns

        data = client.tlds.update(parsed_args.id, data)
        _format_tld(data)
        return six.moves.zip(*sorted(six.iteritems(data)))


class DeleteTLDCommand(command.Command):
    """Delete tld"""

    def get_parser(self, prog_name):
        parser = super(DeleteTLDCommand, self).get_parser(prog_name)

        parser.add_argument('id', help="TLD ID")

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns
        client.tlds.delete(parsed_args.id)

        LOG.info('TLD %s was deleted', parsed_args.id)
