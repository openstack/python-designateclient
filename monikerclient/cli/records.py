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
from monikerclient.v1.records import Record

LOG = logging.getLogger(__name__)


class ListRecordsCommand(base.ListCommand):
    """ List Records """

    def get_parser(self, prog_name):
        parser = super(ListRecordsCommand, self).get_parser(prog_name)

        parser.add_argument('domain_id', help="Domain ID")

        return parser

    def execute(self, parsed_args):
        return self.client.records.list(parsed_args.domain_id)


class GetRecordCommand(base.GetCommand):
    """ Get Record """

    def get_parser(self, prog_name):
        parser = super(GetRecordCommand, self).get_parser(prog_name)

        parser.add_argument('domain_id', help="Domain ID")
        parser.add_argument('id', help="Record ID")

        return parser

    def execute(self, parsed_args):
        return self.client.records.get(parsed_args.domain_id, parsed_args.id)


class CreateRecordCommand(base.CreateCommand):
    """ Create Record """

    def get_parser(self, prog_name):
        parser = super(CreateRecordCommand, self).get_parser(prog_name)

        parser.add_argument('domain_id', help="Domain ID")
        parser.add_argument('--name', help="Record Name", required=True)
        parser.add_argument('--type', help="Record Type", required=True)
        parser.add_argument('--data', help="Record Data", required=True)
        parser.add_argument('--ttl', type=int, help="Record TTL")

        return parser

    def execute(self, parsed_args):
        record = Record(
            name=parsed_args.name,
            type=parsed_args.type,
            data=parsed_args.data,
            ttl=parsed_args.ttl,
        )

        return self.client.records.create(parsed_args.domain_id, record)


class UpdateRecordCommand(base.UpdateCommand):
    """ Update Record """

    def get_parser(self, prog_name):
        parser = super(UpdateRecordCommand, self).get_parser(prog_name)

        parser.add_argument('domain_id', help="Domain ID")
        parser.add_argument('id', help="Record ID")
        parser.add_argument('--name', help="Record Name")
        parser.add_argument('--type', help="Record Type")
        parser.add_argument('--data', help="Record Data")
        parser.add_argument('--ttl', type=int, help="Record TTL")

        return parser

    def execute(self, parsed_args):
        # TODO: API needs updating.. this get is silly
        record = self.client.records.get(parsed_args.domain_id, parsed_args.id)

        # TODO: How do we tell if an arg was supplied or intentionally set to
        #       None?
        record.update({
            'name': parsed_args.name,
            'type': parsed_args.type,
            'data': parsed_args.data,
            'ttl': parsed_args.ttl,
        })

        return self.client.records.update(parsed_args.domain_id, record)


class DeleteRecordCommand(base.DeleteCommand):
    """ Delete Record """

    def get_parser(self, prog_name):
        parser = super(DeleteRecordCommand, self).get_parser(prog_name)

        parser.add_argument('domain_id', help="Domain ID")
        parser.add_argument('id', help="Record ID")

        return parser

    def execute(self, parsed_args):
        return self.client.records.delete(parsed_args.domain_id,
                                          parsed_args.id)
