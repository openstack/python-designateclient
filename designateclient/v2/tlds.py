# Copyright 2015 Hewlett-Packard Development Company, L.P.
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
from designateclient import client


class TLDController(client.Controller):
    def create(self, name, description=None):
        data = {
            'name': name,
        }

        if description is not None:
            data["description"] = description

        return self._post('/tlds', data=data)

    def list(self, criterion=None, marker=None, limit=None):
        url = self.build_url('/tlds', criterion, marker, limit)

        return self._get(url, response_key='tlds')

    def get(self, tld_id):
        url = '/tlds/%s' % tld_id

        return self._get(url)

    def update(self, tld_id, values):
        url = '/tlds/%s' % tld_id

        return self._patch(url, data=values)

    def delete(self, tld_id):
        url = '/tlds/%s' % tld_id

        return self._delete(url)
