"""
 Copyright 2020 Cloudification GmbH. All rights reserved.

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
from designateclient.functionaltests.base import BaseDesignateTest
from designateclient.functionaltests.client import DesignateCLI
from designateclient.functionaltests.datagen import random_zone_name
from designateclient.functionaltests.v2.fixtures import SharedZoneFixture
from designateclient.functionaltests.v2.fixtures import ZoneFixture


class TestSharedZone(BaseDesignateTest):

    def setUp(self):
        super().setUp()
        self.ensure_tld_exists('com')
        fixture = self.useFixture(ZoneFixture(
            name=random_zone_name(),
            email='test@example.com',
        ))
        self.zone = fixture.zone
        self.target_client = DesignateCLI.as_user('alt')

    def test_list_shared_zones(self):
        shared_zone = self.useFixture(SharedZoneFixture(
            zone_id=self.zone.id,
            target_tenant_id=self.target_client.project_id
        )).zone_share

        shared_zones = self.clients.shared_zone_list(self.zone.id)
        self.assertGreater(len(shared_zones), 0)
        self.assertTrue(self._is_entity_in_list(shared_zone, shared_zones))

    def test_share_and_show_shared_zone(self):
        shared_zone = self.useFixture(SharedZoneFixture(
            zone_id=self.zone.id,
            target_tenant_id=self.target_client.project_id
        )).zone_share

        fetched_shared_zone = self.clients.shared_zone_show(self.zone.id,
                                                            shared_zone.id)

        self.assertEqual(
            shared_zone.created_at, fetched_shared_zone.created_at)
        self.assertEqual(shared_zone.id, fetched_shared_zone.id)
        self.assertEqual(
            shared_zone.project_id, fetched_shared_zone.project_id)
        self.assertEqual(shared_zone.zone_id, fetched_shared_zone.zone_id)

    def test_unshare_zone(self):
        shared_zone = self.useFixture(SharedZoneFixture(
            zone_id=self.zone.id,
            target_tenant_id=self.target_client.project_id
        )).zone_share

        shared_zones = self.clients.shared_zone_list(self.zone.id)
        self.assertTrue(self._is_entity_in_list(shared_zone, shared_zones))

        self.clients.unshare_zone(self.zone.id, shared_zone.id)

        shared_zones = self.clients.shared_zone_list(self.zone.id)
        self.assertFalse(self._is_entity_in_list(shared_zone, shared_zones))
