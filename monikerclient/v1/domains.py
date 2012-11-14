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


Domain = warlock.model_factory(utils.load_schema('v1', 'domain'))


class Controller(object):
    def list(self):
        """
        Retrieve a list of domains

        :returns: A list of :class:`Domain`s
        """

    def get(self, domain_id):
        """
        Retrieve a domain

        :param domain_id: Domain Identifier
        :returns: :class:`Domain`
        """

    def create(self, domain):
        """
        Create a domain

        :param domain: A :class:`Domain` to create
        :returns: :class:`Domain`
        """

    def update(self, domain):
        """
        Update a domain

        :param domain: A :class:`Domain` to update
        :returns: :class:`Domain`
        """

    def delete(self, domain):
        """
        Delete a domain

        :param domain: A :class:`Domain`, or Domain Identifier to delete
        """
