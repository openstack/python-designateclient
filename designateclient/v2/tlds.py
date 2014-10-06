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

from designateclient import utils
from designateclient.v1.base import CrudController
from designateclient import warlock


Tld = warlock.model_factory(utils.load_schema('v2', 'tld'))


class TldsController(CrudController):
    def list(self):
        """
        Retrieve a list of tlds

        :returns: A list of :class:`Tld`s
        """
        response = self.client.get('/tlds')

        return [Tld(i) for i in response.json()['tlds']]

    def get(self, tld_id):
        """
        Retrieve a tld

        :param tld_id: Tld Identifier
        :returns: :class:`Tld`
        """
        response = self.client.get('/tlds/%s' % tld_id)

        return Tld(response.json())

    def create(self, tld):
        """
        Create a tld

        :param tld: A :class:`Tld` to create
        :returns: :class:`Tld`
        """
        response = self.client.post('/tlds', data=json.dumps(tld))

        return Tld(response.json())

    def update(self, tld):
        """
        Update a tld

        :param tld: A :class:`Tld` to update
        :returns: :class:`Tld`
        """
        response = self.client.put('/tlds/%s' % tld.id,
                                   data=json.dumps(tld))

        return Tld(response.json())

    def delete(self, tld):
        """
        Delete a tld

        :param tld: A :class:`Tld`, or Tld Identifier to delete
        """
        if isinstance(tld, Tld):
            self.client.delete('/tlds/%s' % tld.id)
        else:
            self.client.delete('/tlds/%s' % tld)
