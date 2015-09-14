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

LOG = logging.getLogger(__name__)


def _format_recordset(recordset):
    # Remove unneeded fields for display output formatting
    recordset['records'] = "\n".join(recordset['records'])
    recordset.pop('links', None)


class ListRecordSetsCommand(lister.Lister):
    """List recordsets"""

    columns = ['id', 'name', 'type', 'records']

    def get_parser(self, prog_name):
        parser = super(ListRecordSetsCommand, self).get_parser(prog_name)

        parser.add_argument('zone_id', help="Zone ID")

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns

        cols = self.columns
        data = client.recordsets.list(parsed_args.zone_id)

        map(_format_recordset, data)
        return cols, (utils.get_item_properties(s, cols) for s in data)


class ShowRecordSetCommand(show.ShowOne):
    """Show recordset details"""

    def get_parser(self, prog_name):
        parser = super(ShowRecordSetCommand, self).get_parser(prog_name)

        parser.add_argument('zone_id', help="Zone ID")
        parser.add_argument('id', help="RecordSet ID")

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns
        data = client.recordsets.get(parsed_args.zone_id, parsed_args.id)

        _format_recordset(data)
        return zip(*sorted(six.iteritems(data)))


class CreateRecordSetCommand(show.ShowOne):
    """Create new recordset"""

    def get_parser(self, prog_name):
        parser = super(CreateRecordSetCommand, self).get_parser(prog_name)

        parser.add_argument('zone_id', help="Zone ID")
        parser.add_argument('name', help="RecordSet Name")
        parser.add_argument('--records', help="RecordSet Records",
                            nargs='+', required=True)
        parser.add_argument('--type', help="RecordSet Type", required=True)
        parser.add_argument('--ttl', type=int, help="Time To Live (Seconds)")
        parser.add_argument('--description', help="Description")

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns

        data = client.recordsets.create(
            parsed_args.zone_id,
            parsed_args.name,
            parsed_args.type,
            parsed_args.records,
            description=parsed_args.description,
            ttl=parsed_args.ttl)

        _format_recordset(data)
        return zip(*sorted(six.iteritems(data)))


class SetRecordSetCommand(show.ShowOne):
    """Set recordset properties"""

    def get_parser(self, prog_name):
        parser = super(SetRecordSetCommand, self).get_parser(prog_name)

        parser.add_argument('zone_id', help="Zone ID")
        parser.add_argument('id', help="RecordSet ID")
        parser.add_argument('--name', help="RecordSet Name")
        parser.add_argument('--records', help="Records", nargs='+')

        description_group = parser.add_mutually_exclusive_group()
        description_group.add_argument('--description', help="Description")
        description_group.add_argument('--no-description', action='store_true')

        ttl_group = parser.add_mutually_exclusive_group()
        ttl_group.add_argument('--ttl', type=int, help="TTL")
        ttl_group.add_argument('--no-ttl', action='store_true')

        return parser

    def take_action(self, parsed_args):
        data = {}

        if parsed_args.name:
            data['name'] = parsed_args.name

        if parsed_args.no_description:
            data['description'] = None
        elif parsed_args.description:
            data['description'] = parsed_args.description

        if parsed_args.no_ttl:
            data['ttl'] = None
        elif parsed_args.ttl:
            data['ttl'] = parsed_args.ttl

        if parsed_args.records:
            data['records'] = parsed_args.records

        client = self.app.client_manager.dns

        updated = client.recordsets.update(
            parsed_args.zone_id,
            parsed_args.id,
            data)

        _format_recordset(updated)

        return zip(*sorted(six.iteritems(updated)))


class DeleteRecordSetCommand(command.Command):
    """Delete recordset"""

    def get_parser(self, prog_name):
        parser = super(DeleteRecordSetCommand, self).get_parser(prog_name)

        parser.add_argument('zone_id', help="Zone ID")
        parser.add_argument('id', help="RecordSet ID")

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dns
        client.recordsets.delete(parsed_args.zone_id, parsed_args.id)

        LOG.info('RecordSet %s was deleted', parsed_args.id)
