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
from __future__ import absolute_import

import fixtures
from tempest_lib.exceptions import CommandFailed

from designateclient.functionaltests.client import DesignateCLI


class BaseFixture(fixtures.Fixture):

    def __init__(self, user='default', *args, **kwargs):
        """args/kwargs are forwarded to a create method on DesignateCLI"""
        super(BaseFixture, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.client = DesignateCLI.as_user(user)


class ZoneFixture(BaseFixture):
    """See DesignateCLI.zone_create for __init__ args"""

    def _setUp(self):
        super(ZoneFixture, self)._setUp()
        self.zone = self.client.zone_create(*self.args, **self.kwargs)
        self.addCleanup(self.cleanup_zone, self.client, self.zone.id)

    @classmethod
    def cleanup_zone(cls, client, zone_id):
        try:
            client.zone_delete(zone_id)
        except CommandFailed:
            pass


class TransferRequestFixture(BaseFixture):
    """See DesignateCLI.zone_transfer_request_create for __init__ args"""

    def __init__(self, zone, user='default', target_user='alt', *args,
                 **kwargs):
        super(TransferRequestFixture, self).__init__(user, *args, **kwargs)
        self.zone = zone
        self.target_client = DesignateCLI.as_user(target_user)

        # the client has a bug such that it requires --target-project-id.
        # when this bug is fixed, please remove this
        self.kwargs['target_project_id'] = self.target_client.project_id

    def _setUp(self):
        super(TransferRequestFixture, self)._setUp()
        self.transfer_request = self.client.zone_transfer_request_create(
            zone_id=self.zone.id,
            *self.args, **self.kwargs
        )
        self.addCleanup(self.cleanup_transfer_request, self.client,
                        self.transfer_request.id)
        self.addCleanup(ZoneFixture.cleanup_zone, self.client, self.zone.id)
        self.addCleanup(ZoneFixture.cleanup_zone, self.target_client,
                        self.zone.id)

    @classmethod
    def cleanup_transfer_request(cls, client, transfer_request_id):
        try:
            client.zone_transfer_request_delete(transfer_request_id)
        except CommandFailed:
            pass


class RecordsetFixture(BaseFixture):
    """See DesignateCLI.recordset_create for __init__ args"""

    def _setUp(self):
        super(RecordsetFixture, self)._setUp()
        self.recordset = self.client.recordset_create(
            *self.args, **self.kwargs)
        self.addCleanup(self.cleanup_recordset, self.client,
                        self.recordset.zone_id, self.recordset.id)

    @classmethod
    def cleanup_recordset(cls, client, zone_id, recordset_id):
        try:
            client.recordset_delete(zone_id, recordset_id)
        except CommandFailed:
            pass


class TLDFixture(BaseFixture):
    """See DesignateCLI.tld_create for __init__ args"""

    def __init__(self, user='admin', *args, **kwargs):
        super(TLDFixture, self).__init__(user=user, *args, **kwargs)

    def _setUp(self):
        super(TLDFixture, self)._setUp()
        self.tld = self.client.tld_create(*self.args, **self.kwargs)
        self.addCleanup(self.cleanup_tld, self.client, self.tld.id)

    @classmethod
    def cleanup_tld(cls, client, tld_id):
        try:
            client.tld_delete(tld_id)
        except CommandFailed:
            pass


class BlacklistFixture(BaseFixture):
    """See DesignateCLI.zone_blacklist_create for __init__ args"""

    def __init__(self, user='admin', *args, **kwargs):
        super(BlacklistFixture, self).__init__(user=user, *args, **kwargs)

    def _setUp(self):
        super(BlacklistFixture, self)._setUp()
        self.blacklist = self.client.zone_blacklist_create(*self.args,
                                                           **self.kwargs)
        self.addCleanup(self.cleanup_blacklist, self.client, self.blacklist.id)

    @classmethod
    def cleanup_blacklist(cls, client, blacklist_id):
        try:
            client.zone_blacklist_delete(blacklist_id)
        except CommandFailed:
            pass
