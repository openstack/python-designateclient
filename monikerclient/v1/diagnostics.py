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
from monikerclient.v1.base import Controller


# NOTE(kiall): The /../ is an awful hack.. But keystone only gives us a
#              versioned endpoint. Maybe we should make the diags calls part
#              of v1?
class DiagnosticsController(Controller):
    def ping(self, service, host):
        """
        Ping a service on a given host
        """
        response = self.client.get('/../diagnostics/ping/%s/%s' %
                                   (service, host))

        return response.json

    def sync_all(self):
        """
        Sync Everything
        """
        response = self.client.post('/../diagnostics/sync/all')

        return response.json

    def sync_domain(self, domain_id):
        """
        Sync Single Domain
        """
        response = self.client.post('/../diagnostics/sync/domain/%s' %
                                    domain_id)

        return response.json

    def sync_record(self, domain_id, record_id):
        """
        Sync Single Record
        """
        response = self.client.post('/../diagnostics/sync/record/%s/%s' %
                                    (domain_id, record_id))

        return response.json
