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


def _format_blacklist(blacklist):
    # Remove unneeded fields for display output formatting
    blacklist.pop('links', None)


class ListBlacklistsCommand(lister.Lister):
    """List blacklists"""

    columns = ['id', 'pattern', 'description']

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns

        cols = self.columns
        data = get_all(client.blacklists.list)
        return cols, (utils.get_item_properties(s, cols) for s in data)


class ShowBlacklistCommand(show.ShowOne):
    """Show blacklist details"""

    def get_parser(self, prog_name):
        parser = super(ShowBlacklistCommand, self).get_parser(prog_name)

        parser.add_argument('id', help="Blacklist ID")

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns
        data = client.blacklists.get(parsed_args.id)
        _format_blacklist(data)
        return six.moves.zip(*sorted(six.iteritems(data)))


class CreateBlacklistCommand(show.ShowOne):
    """Create new blacklist"""

    def get_parser(self, prog_name):
        parser = super(CreateBlacklistCommand, self).get_parser(prog_name)

        parser.add_argument('--pattern', help="Blacklist pattern",
                            required=True)
        parser.add_argument('--description', help="Description")

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns

        data = client.blacklists.create(
            parsed_args.pattern, parsed_args.description)

        _format_blacklist(data)
        return six.moves.zip(*sorted(six.iteritems(data)))


class SetBlacklistCommand(show.ShowOne):
    """Set blacklist properties"""

    def get_parser(self, prog_name):
        parser = super(SetBlacklistCommand, self).get_parser(prog_name)

        parser.add_argument('id', help="Blacklist ID")
        parser.add_argument('--pattern', help="Blacklist pattern")

        description_group = parser.add_mutually_exclusive_group()
        description_group.add_argument('--description', help="Description")
        description_group.add_argument('--no-description', action='store_true')

        return parser

    def take_action(self, parsed_args):
        data = {}

        if parsed_args.pattern:
            data['pattern'] = parsed_args.pattern

        if parsed_args.no_description:
            data['description'] = None
        elif parsed_args.description:
            data['description'] = parsed_args.description

        client = self.app.client_manager.dns

        updated = client.blacklists.update(parsed_args.id, data)

        _format_blacklist(updated)
        return six.moves.zip(*sorted(six.iteritems(updated)))


class DeleteBlacklistCommand(command.Command):
    """Delete blacklist"""

    def get_parser(self, prog_name):
        parser = super(DeleteBlacklistCommand, self).get_parser(prog_name)

        parser.add_argument('id', help="Blacklist ID")

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns
        client.blacklists.delete(parsed_args.id)

        LOG.info('Blacklist %s was deleted', parsed_args.id)
