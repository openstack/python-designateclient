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

from unittest import mock

from osc_lib.tests import utils

from designateclient.tests.osc import resources
from designateclient.v2 import base
from designateclient.v2.cli import recordsets


class TestDesignateCreateRecordSets(utils.TestCommand):
    def setUp(self):
        super(TestDesignateCreateRecordSets, self).setUp()
        self.app.client_manager.dns = mock.MagicMock()
        self.cmd = recordsets.CreateRecordSetCommand(self.app, None)
        self.dns_client = self.app.client_manager.dns

    def test_create_recordset(self):
        arg_list = [
            '6f106adb-0896-4114-b34f-4ac8dfee9465',
            'example',
            '--type', 'A',
            '--record', '127.0.0.1',
            '--record', '127.0.0.2',
        ]
        verify_args = [
            ('zone_id', '6f106adb-0896-4114-b34f-4ac8dfee9465'),
            ('name', 'example'),
            ('type', 'A'),
            ('record', ['127.0.0.1', '127.0.0.2']),
        ]

        body = resources.load('recordset_create')
        self.dns_client.recordsets.create.return_value = body

        parsed_args = self.check_parser(self.cmd, arg_list, verify_args)
        columns, data = self.cmd.take_action(parsed_args)

        results = list(data)

        self.assertEqual(14, len(results))


class TestDesignateListRecordSets(utils.TestCommand):
    def setUp(self):
        super(TestDesignateListRecordSets, self).setUp()
        self.app.client_manager.dns = mock.MagicMock()
        self.cmd = recordsets.ListRecordSetsCommand(self.app, None)
        self.dns_client = self.app.client_manager.dns

    def test_list_recordsets(self):
        arg_list = ['6f106adb-0896-4114-b34f-4ac8dfee9465']
        verify_args = [
            ('zone_id', '6f106adb-0896-4114-b34f-4ac8dfee9465'),
        ]

        body = resources.load('recordset_list')
        result = base.DesignateList()
        result.extend(body['recordsets'])

        self.dns_client.recordsets.list.return_value = result

        parsed_args = self.check_parser(self.cmd, arg_list, verify_args)
        columns, data = self.cmd.take_action(parsed_args)

        results = list(data)

        self.assertEqual(3, len(results))

    def test_list_all_recordsets(self):
        arg_list = ['all']
        verify_args = [
            ('zone_id', 'all'),
        ]

        body = resources.load('recordset_list_all')
        result = base.DesignateList()
        result.extend(body['recordsets'])

        self.dns_client.recordsets.list_all_zones.return_value = result

        parsed_args = self.check_parser(self.cmd, arg_list, verify_args)
        columns, data = self.cmd.take_action(parsed_args)

        results = list(data)

        self.assertEqual(5, len(results))
