# Copyright 2025 Red Hat
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
import uuid

from designateclient.tests import v2


class TestQuotas(v2.APIV2TestCase, v2.CrudMixin):
    RESOURCE = 'quotas'

    def test_list(self):
        ref = {"zones": 100}

        self.stub_url("GET", parts=[self.RESOURCE], json=ref)

        response = self.client.quotas.list()
        self.assertEqual(ref, response)

    def test_list_with_project_id(self):
        project_id = uuid.uuid4().hex
        ref = {"zones": 100}

        self.stub_url("GET", parts=[self.RESOURCE, project_id], json=ref)

        response = self.client.quotas.list(project_id)
        self.assertEqual(ref, response)

    def test_update(self):
        project_id = uuid.uuid4().hex
        ref = {"zones": 100}

        self.stub_url("PATCH", parts=[self.RESOURCE, project_id], json=ref)

        values = {"zones": 100}
        self.client.quotas.update(project_id, values)
        self.assertRequestBodyIs(json=values)

    def test_reset(self):
        project_id = uuid.uuid4().hex

        self.stub_url("DELETE", parts=[self.RESOURCE, project_id])

        self.client.quotas.reset(project_id)
        self.assertRequestBodyIs(None)
