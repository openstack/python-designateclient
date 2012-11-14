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
from monikerclient import warlock
from monikerclient import utils


Server = warlock.model_factory(utils.load_schema('v1', 'server'))


class Controller(object):
    def list(self):
        """
        Retrieve a list of servers

        :returns: A list of :class:`Server`s
        """

    def get(self, server_id):
        """
        Retrieve a server

        :param server_id: Server Identifier
        :returns: :class:`Server`
        """

    def create(self, server):
        """
        Create a server

        :param server: A :class:`Server` to create
        :returns: :class:`Server`
        """

    def update(self, server):
        """
        Update a server

        :param server: A :class:`Server` to update
        :returns: :class:`Server`
        """

    def delete(self, server):
        """
        Delete a server

        :param server: A :class:`Server`, or Server Identifier to delete
        """
