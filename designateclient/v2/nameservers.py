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
from designateclient.v2.base import V2Controller
from designateclient.v2 import utils as v2_utils


class NameServerController(V2Controller):
    def list(self, zone):
        zone = v2_utils.resolve_by_name(self.client.zones.list, zone)

        url = f'/zones/{zone}/nameservers'

        return self._get(url, response_key='nameservers')
