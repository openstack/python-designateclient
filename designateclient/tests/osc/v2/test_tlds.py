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

from designateclient.v2 import base
from designateclient.v2.cli import tlds


class TestDesignateListTLDs(utils.TestCommand):
    def setUp(self):
        super().setUp()
        self.app.client_manager.dns = mock.MagicMock()
        self.cmd = tlds.ListTLDsCommand(self.app, None)
        self.dns_client = self.app.client_manager.dns

    def test_list_tlds(self):
        arg_list = []
        verify_args = []

        result = base.DesignateList()
        result.extend([
            {'id': '1', 'name': 'com', 'description': None},
            {'id': '2', 'name': 'org', 'description': None},
        ])

        self.dns_client.tlds.list.return_value = result

        parsed_args = self.check_parser(self.cmd, arg_list, verify_args)
        columns, data = self.cmd.take_action(parsed_args)

        results = list(data)

        self.assertEqual(2, len(results))
        self.dns_client.tlds.list.assert_called_once_with(criterion={})

    def test_list_tlds_with_name_filter(self):
        arg_list = ['--name', 'com']
        verify_args = [('name', 'com')]

        result = base.DesignateList()
        result.extend([
            {'id': '1', 'name': 'com', 'description': None},
        ])

        self.dns_client.tlds.list.return_value = result

        parsed_args = self.check_parser(self.cmd, arg_list, verify_args)
        columns, data = self.cmd.take_action(parsed_args)

        results = list(data)

        self.assertEqual(1, len(results))
        self.dns_client.tlds.list.assert_called_once_with(
            criterion={'name': 'com'}
        )
