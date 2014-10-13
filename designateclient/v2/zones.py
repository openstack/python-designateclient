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
import pdb

from designateclient import utils
from designateclient.v1.base import CrudController
from designateclient import warlock


Zone = warlock.model_factory(utils.load_schema('v2', 'zone'))


class ZonesController(CrudController):
    def list(self):
        """
        Retrieve a list of zones

        :returns: A list of :class:`Zone`s
        """
        response = self.client.get('/zones')

        return [Zone(i) for i in response.json()['zones']]

    def get(self, zone_id):
        """
        Retrieve a zone

        :param zone_id: Zone Identifier
        :returns: :class:`Zone`
        """
        response = self.client.get('/zones/%s' % zone_id)

        return Zone(response.json())

    def create(self, zone):
        """
        Create a zone

        :param zone: A :class:`Zone` to create
        :returns: :class:`Zone`
        """
        response = self.client.post('/zones', data=json.dumps(zone))

        return Zone(response.json())

    def update(self, zone):
        """
        Update a zone

        :param zone: A :class:`Zone` to update
        :returns: :class:`Zone`
        """
        pdb.set_trace()
        id = zone['zone']['id']                                                  
        del zone['zone']['id']                                                   
        response = self.client.patch('/zones/%s' % id,                          
                                   data=json.dumps(zone))                       
                                                                               
        return Zone(response.json())

    def delete(self, zone):
        """
        Delete a zone

        :param zone: A :class:`Zone`, or Zone Identifier to delete
        """
        if isinstance(zone, Zone):
            self.client.delete('/zones/%s' % zone.id)
        else:
            self.client.delete('/zones/%s' % zone)

