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


class Controller(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, client):
        self.client = client

    def list(self, *args, **kw):
        """
        List something
        """
        raise NotImplementedError

    def get(self, *args, **kw):
        """
        Get something
        """
        raise NotImplementedError

    def create(self, *args, **kw):
        """
        Create something
        """
        raise NotImplementedError

    def update(self, *args, **kw):
        """
        Update something
        """
        raise NotImplementedError

    def delete(self, *args, **kw):
        """
        Delete something
        """
        raise NotImplementedError
