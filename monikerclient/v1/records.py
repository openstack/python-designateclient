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
import json
from monikerclient import warlock
from monikerclient import utils
from monikerclient.v1.base import Controller


Record = warlock.model_factory(utils.load_schema('v1', 'record'))


class RecordsController(Controller):
    def list(self):
        """
        Retrieve a list of records

        :returns: A list of :class:`Record`s
        """
        response = self.client.get('/records')

        return [Record(i) for i in response.json['records']]

    def get(self, record_id):
        """
        Retrieve a record

        :param record_id: Record Identifier
        :returns: :class:`Record`
        """
        response = self.client.get('/records/%s' % record_id)

        return Record(response.json)

    def create(self, record):
        """
        Create a record

        :param record: A :class:`Record` to create
        :returns: :class:`Record`
        """
        response = self.client.post('/records', data=json.dumps(record))

        return record.update(response.json)

    def update(self, record):
        """
        Update a record

        :param record: A :class:`Record` to update
        :returns: :class:`Record`
        """
        response = self.client.put('/records/%s' % record.id,
                                   data=json.dumps(record))

        return record.update(response.json)

    def delete(self, record):
        """
        Delete a record

        :param record: A :class:`Record`, or Record Identifier to delete
        """
        if isinstance(record, Record):
            self.client.delete('/records/%s' % record.id)
        else:
            self.client.delete('/records/%s' % record)
