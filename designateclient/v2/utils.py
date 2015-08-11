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
from oslo_utils import uuidutils

from designateclient import exceptions


def resolve_by_name(func, name, *args):
    """
    Helper to resolve a "name" a'la foo.com to it's ID by using REST api's
    query support and filtering on name.
    """
    if uuidutils.is_uuid_like(name):
        return name

    results = func(criterion={"name": "%s" % name}, *args)
    length = len(results)

    if length == 1:
        return results[0]["id"]
    elif length == 0:
        raise exceptions.NotFound("Name %s didn't resolve" % name)
    else:
        msg = "Multiple matches found for %s, please use ID instead." % name
        raise exceptions.NoUniqueMatch(msg)
