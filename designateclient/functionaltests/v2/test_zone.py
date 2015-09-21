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
from designateclient.functionaltests.v2.fixtures import ZoneFixture


class TestZone(BaseDesignateTest):

    def setUp(self):
        super(TestZone, self).setUp()
        self.fixture = self.useFixture(ZoneFixture(
            name=random_zone_name(),
            email='test@example.com',
        ))
        self.zone = self.fixture.zone

    def test_zone_list(self):
        zones = self.clients.zone_list()
        self.assertGreater(len(zones), 0)

    def test_zone_create_and_show(self):
        zone = self.clients.zone_show(self.zone.id)
        self.assertTrue(hasattr(zone, 'action'))
        self.assertEqual(zone.created_at, self.zone.created_at)
        self.assertEqual(zone.description, self.zone.description)
        self.assertEqual(zone.email, self.zone.email)
        self.assertEqual(zone.id, self.zone.id)
        self.assertEqual(zone.masters, self.zone.masters)
        self.assertEqual(zone.name, self.zone.name)
        self.assertEqual(zone.pool_id, self.zone.pool_id)
        self.assertEqual(zone.project_id, self.zone.project_id)
        self.assertEqual(zone.serial, self.zone.serial)
        self.assertTrue(hasattr(zone, 'status'))
        self.assertEqual(zone.transferred_at, self.zone.transferred_at)
        self.assertEqual(zone.ttl, self.zone.ttl)
        self.assertEqual(zone.type, self.zone.type)
        self.assertEqual(zone.updated_at, self.zone.updated_at)
        self.assertEqual(zone.version, self.zone.version)

    def test_zone_delete(self):
        self.clients.zone_delete(self.zone.id)
        self.assertRaises(CommandFailed, self.clients.zone_show, self.zone.id)

    def test_zone_set(self):
        ttl = int(self.zone.ttl) + 123
        email = 'updated{0}'.format(self.zone.email)
        description = 'new description'

        zone = self.clients.zone_set(self.zone.id, ttl=ttl, email=email,
                                     description=description)
        self.assertEqual(int(zone.ttl), ttl)
        self.assertEqual(zone.email, email)
        self.assertEqual(zone.description, description)

    def test_invalid_option_on_zone_create(self):
        cmd = 'zone create %s --invalid "not a valid option"'.format(
            random_zone_name())
        self.assertRaises(CommandFailed, self.clients.openstack, cmd)

    def test_invalid_zone_command(self):
        cmd = 'zone hopefullynotacommand'
        self.assertRaises(CommandFailed, self.clients.openstack, cmd)


class TestsPassingZoneFlags(BaseDesignateTest):

    def test_zone_create_primary_with_all_args(self):
        zone_name = random_zone_name()
        fixture = self.useFixture(ZoneFixture(
            name=zone_name,
            email='primary@example.com',
            description='A primary zone',
            ttl=2345,
            type='PRIMARY',
        ))
        zone = fixture.zone
        self.assertEqual(zone.name, zone_name)
        self.assertEqual(zone.email, 'primary@example.com')
        self.assertEqual(zone.description, 'A primary zone')
        self.assertEqual(zone.ttl, '2345')
        self.assertEqual(zone.type, 'PRIMARY')

    def test_zone_create_secondary_with_all_args(self):
        zone_name = random_zone_name()
        fixture = self.useFixture(ZoneFixture(
            name=zone_name,
            description='A secondary zone',
            type='SECONDARY',
            masters='127.0.0.1',
        ))
        zone = fixture.zone
        self.assertEqual(zone.name, zone_name)
        self.assertEqual(zone.description, 'A secondary zone')
        self.assertEqual(zone.type, 'SECONDARY')
        self.assertEqual(zone.masters, '127.0.0.1')

    def test_zone_set_secondary_masters(self):
        fixture = self.useFixture(ZoneFixture(
            name=random_zone_name(),
            description='A secondary zone',
            type='SECONDARY',
            masters='127.0.0.1',
        ))
        zone = fixture.zone
        self.assertEqual(zone.masters, '127.0.0.1')

        zone = self.clients.zone_set(zone.id, masters='127.0.0.2')
        self.assertEqual(zone.masters, '127.0.0.2')
