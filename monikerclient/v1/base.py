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
import abc
import json


class Controller(object):
    __metaclass__ = abc.ABCMeta

    resource = None
    schema = None

    def __init__(self, client):
        self.client = client

    @property
    def path(self):
        return '/' + self.plural

    @property
    def plural(self):
        return self.resource + 's'

    def _list(self):
        """
        List something
        """
        response = self.client.get(self.path)
        return [self.schema(i) for i in response.json[self.plural]]

    def _get(self, id_):
        """
        Get something
        """
        response = self.client.get(self.path + '/%s' % id_)
        return self.schema(response.json)

    def _create(self, values):
        """
        Create something
        """
        response = self.client.post(self.path, data=json.dumps(values))
        return self.schema(response.json)

    def _update(self, values):
        """
        Update something
        """
        response = self.client.put(self.path + '/%s' % values['id'],
                                   data=json.dumps(values))
        return self.schema(response.json)

    def _delete(self, obj):
        """
        Delete something
        """
        id_ = obj.id if isinstance(obj, self.schema) else obj
        response = self.client.delete(self.path + '/%s' % id_)

    @abc.abstractmethod
    def list(self, *args, **kw):
        """
        List a resource
        """

    @abc.abstractmethod
    def get(self, *args, **kw):
        """
        Get a resouce
        """

    @abc.abstractmethod
    def create(self, *args, **kw):
        """
        Create a resource
        """

    @abc.abstractmethod
    def update(self, *args, **kw):
        """
        Update a resource
        """

    @abc.abstractmethod
    def delete(self, *args, **kw):
        """
        Delete a resource
        """
