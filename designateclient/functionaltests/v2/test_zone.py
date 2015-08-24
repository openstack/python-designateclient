"""
Copyright 2015 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from tempest_lib.exceptions import CommandFailed

from designateclient.functionaltests.base import BaseDesignateTest
from designateclient.functionaltests.datagen import random_zone_name


class TestZone(BaseDesignateTest):

    def setUp(self):
        super(TestZone, self).setUp()
        self.zone_name = random_zone_name()
        zone = self.clients.zone_create(name=self.zone_name,
                                        email='test@example.com')
        self.zone_id = zone.id

    def test_zone_list(self):
        zones = self.clients.zone_list()
        self.assertGreater(len(zones), 0)

    def test_zone_create_and_show(self):
        zone = self.clients.zone_show(self.zone_id)
        self.assertEqual(zone.name, self.zone_name)
        self.assertEqual(zone.id, self.zone_id)

    def test_zone_delete(self):
        self.clients.zone_delete(self.zone_id)
        self.assertRaises(CommandFailed, self.clients.zone_show, self.zone_id)

    def tearDown(self):
        if hasattr(self, 'zone_id'):
            self.clients.zone_delete(self.zone_id, fail_ok=True)
        super(TestZone, self).tearDown()
