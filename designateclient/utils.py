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

import uuid

from keystoneauth1 import adapter

from designateclient import exceptions


def get_item_properties(item, fields, mixed_case_fields=(), formatters=None):
    """Return a tuple containing the item properties.

    :param item: a single item resource (e.g. Server, Tenant, etc)
    :param fields: tuple of strings with the desired field names
    :param mixed_case_fields: tuple of field names to preserve case
    :param formatters: dictionary mapping field names to callables
        to format the values
    """
    if formatters is None:
        formatters = {}
    row = []

    for field in fields:
        if field in formatters:
            row.append(formatters[field](item))
        else:
            if field in mixed_case_fields:
                field_name = field.replace(' ', '_')
            else:
                field_name = field.lower().replace(' ', '_')
            if not hasattr(item, field_name) and \
                    (isinstance(item, dict) and field_name in item):
                data = item[field_name]
            else:
                data = getattr(item, field_name, '')
            if data is None:
                data = ''
            row.append(data)
    return tuple(row)


def get_columns(data):
    """
    Some row's might have variable count of columns, ensure that we have the
    same.

    :param data: Results in [{}, {]}]
    """
    columns = set()

    def _seen(col):
        columns.add(str(col))

    map(lambda item: map(_seen, list(item.keys())), data)
    return list(columns)


def find_resourceid_by_name_or_id(resource_client, name_or_id):
    """Find resource id from its id or name."""
    try:
        # Try to return an uuid
        return str(uuid.UUID(name_or_id))
    except ValueError:
        # Not an uuid => assume it is resource name
        pass

    resources = resource_client.list()
    candidate_ids = [r['id'] for r in resources if r.get('name') == name_or_id]
    if not candidate_ids:
        raise exceptions.ResourceNotFound(
            'Could not find resource with name "%s"' % name_or_id)
    elif len(candidate_ids) > 1:
        str_ids = ','.join(candidate_ids)
        raise exceptions.NoUniqueMatch(
            'Multiple resources with name "%s": %s' % (name_or_id, str_ids))
    return candidate_ids[0]


class AdapterWithTimeout(adapter.Adapter):
    """adapter.Adapter wraps around a Session.

    The user can pass a timeout keyword that will apply only to
    the Designate Client, in order:

    - timeout keyword passed to ``request()``
    - timeout keyword passed to ``AdapterWithTimeout()``
    - timeout attribute on keystone session
    """
    def __init__(self, *args, **kw):
        self.timeout = kw.pop('timeout', None)
        super(self.__class__, self).__init__(*args, **kw)

    def request(self, *args, **kwargs):
        if self.timeout is not None:
            kwargs.setdefault('timeout', self.timeout)

        return super(AdapterWithTimeout, self).request(*args, **kwargs)
