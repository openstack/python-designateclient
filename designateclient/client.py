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


import six


@six.add_metaclass(abc.ABCMeta)
class Controller(object):

    def __init__(self, client):
        self.client = client


@six.add_metaclass(abc.ABCMeta)
class CrudController(Controller):

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
