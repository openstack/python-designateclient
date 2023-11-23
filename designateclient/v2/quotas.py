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


class QuotasController(V2Controller):
    def list(self, project_id):
        return self._get(f'/quotas/{project_id}')

    def update(self, project_id, values):
        return self._patch(f'/quotas/{project_id}', data=values)

    def reset(self, project_id):
        return self._delete(f'/quotas/{project_id}')
