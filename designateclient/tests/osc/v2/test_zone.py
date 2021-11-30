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
from designateclient.v2.cli import zones


class TestDesignateCreateZone(utils.TestCommand):
    def setUp(self):
        super(TestDesignateCreateZone, self).setUp()
        self.app.client_manager.dns = mock.MagicMock()
        self.cmd = zones.CreateZoneCommand(self.app, None)
        self.dns_client = self.app.client_manager.dns

    def test_create_zone(self):
        arg_list = [
            'example.devstack.org.',
            '--email', 'fake@devstack.org',
        ]
        verify_args = [
            ('name', 'example.devstack.org.'),
            ('email', 'fake@devstack.org'),
        ]

        body = resources.load('zone_create')
        self.dns_client.zones.create.return_value = body

        parsed_args = self.check_parser(self.cmd, arg_list, verify_args)
        columns, data = self.cmd.take_action(parsed_args)

        results = list(data)

        self.assertEqual(17, len(results))


class TestDesignateListZones(utils.TestCommand):
    def setUp(self):
        super(TestDesignateListZones, self).setUp()
        self.app.client_manager.dns = mock.MagicMock()
        self.cmd = zones.ListZonesCommand(self.app, None)
        self.dns_client = self.app.client_manager.dns

    def test_list_zones(self):
        arg_list = []
        verify_args = []

        body = resources.load('zone_list')
        result = base.DesignateList()
        result.extend(body['zones'])

        self.dns_client.zones.list.return_value = result

        parsed_args = self.check_parser(self.cmd, arg_list, verify_args)
        columns, data = self.cmd.take_action(parsed_args)

        results = list(data)

        self.assertEqual(2, len(results))
