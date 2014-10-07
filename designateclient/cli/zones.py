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
from designateclient.v2.zones import Zone

import pdb

LOG = logging.getLogger(__name__)


class ListZonesCommand(base.ListCommand):
    """List Zones"""

    columns = ['id', 'name', 'serial']

    def execute(self, parsed_args):
        return self.client.zones.list()


class GetZoneCommand(base.GetCommand):
    """Get Zone"""

    def get_parser(self, prog_name):
        parser = super(GetZoneCommand, self).get_parser(prog_name)

        parser.add_argument('id', help="Zone ID")

        return parser

    def execute(self, parsed_args):
        return self.client.zones.get(parsed_args.id)


class CreateZoneCommand(base.CreateCommand):
    """Create Zone"""

    def get_parser(self, prog_name):
        parser = super(CreateZoneCommand, self).get_parser(prog_name)

        parser.add_argument('--name', help="Zone Name", required=True)
        parser.add_argument('--email', help="Zone Email", required=True)
        parser.add_argument('--ttl', type=int, help="Time To Live (Seconds)")
        parser.add_argument('--description', help="Description")

        return parser

    def execute(self, parsed_args):
        zone = Zone(
            name=parsed_args.name,
            email=parsed_args.email,
        )

        if parsed_args.description:
            zone.description = parsed_args.description

        if parsed_args.ttl:
            zone.ttl = parsed_args.ttl

        zone = {'zone': zone}
        return self.client.zones.create(zone)


class UpdateZoneCommand(base.UpdateCommand):
    """Update Zone"""

    def get_parser(self, prog_name):
        parser = super(UpdateZoneCommand, self).get_parser(prog_name)

        parser.add_argument('id', help="Zone ID")
        parser.add_argument('--name', help="Zone Name")
        parser.add_argument('--email', help="Zone Email")
        parser.add_argument('--ttl', type=int, help="Time To Live (Seconds)")
        description_group = parser.add_mutually_exclusive_group()
        description_group.add_argument('--description', help="Description")
        description_group.add_argument('--no-description', action='store_true')

        return parser

    def execute(self, parsed_args):
        pdb.set_trace()
        zone = self.client.zones.get(parsed_args.id)

        if parsed_args.name:
            zone.name = parsed_args.name

        if parsed_args.email:
            zone.email = parsed_args.email

        if parsed_args.ttl:
            zone.ttl = parsed_args.ttl

        if parsed_args.no_description:
            zone.description = None
        elif parsed_args.description:
            zone.description = parsed_args.description

        zone = {'zone': zone}
        pdb.set_trace()
        return self.client.zones.update(zone)


class DeleteZoneCommand(base.DeleteCommand):
    """Delete Zone"""

    def get_parser(self, prog_name):
        parser = super(DeleteZoneCommand, self).get_parser(prog_name)

        parser.add_argument('id', help="Zone ID")

        return parser

    def execute(self, parsed_args):
        return self.client.zones.delete(parsed_args.id)


