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
from keystoneclient import adapter

from designateclient import exceptions
from designateclient.v2.blacklists import BlacklistController
from designateclient.v2.limits import LimitController
from designateclient.v2.nameservers import NameServerController
from designateclient.v2.recordsets import RecordSetController
from designateclient.v2.reverse import FloatingIPController
from designateclient.v2.tlds import TLDController
from designateclient.v2.zones import ZoneController
from designateclient.v2.zones import ZoneTransfersController
from designateclient import version


class DesignateAdapter(adapter.LegacyJsonAdapter):
    """
    Adapter around LegacyJsonAdapter.
    """
    def request(self, *args, **kwargs):
        kwargs.setdefault('raise_exc', False)

        kwargs.setdefault('headers', {}).setdefault(
            'Content-Type', 'application/json')
        response, body = super(DesignateAdapter, self).request(*args, **kwargs)

        # Decode is response, if possible
        try:
            response_payload = response.json()
        except ValueError:
            response_payload = {}

        if response.status_code == 400:
            raise exceptions.BadRequest(**response_payload)
        elif response.status_code in (401, 403):
            raise exceptions.Forbidden(**response_payload)
        elif response.status_code == 404:
            raise exceptions.NotFound(**response_payload)
        elif response.status_code == 409:
            raise exceptions.Conflict(**response_payload)
        elif response.status_code >= 500:
            raise exceptions.Unknown(**response_payload)
        return response, body


class Client(object):
    def __init__(self, region_name=None, endpoint_type='publicURL',
                 extensions=None, service_type='dns', service_name=None,
                 http_log_debug=False, session=None, auth=None):
        self.session = DesignateAdapter(
            session,
            auth=auth,
            region_name=region_name,
            service_type=service_type,
            interface=endpoint_type.rstrip('URL'),
            user_agent='python-designateclient-%s' % version.version_info,
            version=('2'))

        self.blacklists = BlacklistController(self)
        self.floatingips = FloatingIPController(self)
        self.limits = LimitController(self)
        self.nameservers = NameServerController(self)
        self.recordsets = RecordSetController(self)
        self.tlds = TLDController(self)
        self.zones = ZoneController(self)
        self.zone_transfers = ZoneTransfersController(self)
