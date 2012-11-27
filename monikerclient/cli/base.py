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
from cliff.command import Command as CliffCommand
from cliff.lister import Lister
from cliff.show import ShowOne
from monikerclient import utils
from monikerclient.v1 import Client


class Command(CliffCommand):
    __metaclass__ = abc.ABCMeta

    def run(self, parsed_args):
        client_args = {
            'endpoint': self.app.options.os_endpoint,
            'auth_url': self.app.options.os_auth_url,
            'username': self.app.options.os_username,
            'password': self.app.options.os_password,
            'tenant_id': self.app.options.os_tenant_id,
            'tenant_name': self.app.options.os_tenant_name,
            'token': self.app.options.os_token,
            'region_name': self.app.options.os_region_name,
        }

        self.client = Client(**client_args)

        return super(Command, self).run(parsed_args)

    @abc.abstractmethod
    def execute(self, parsed_args):
        """
        Execute something, this is since we overload self.take_action()
        in order to format the data

        This method __NEEDS__ to be overloaded!

        :param parsed_args: The parsed args that are given by take_action()
        """

    def post_execute(self, data):
        """
        Format the results locally if needed, by default we just return data

        :param data: Whatever is returned by self.execute()
        """
        return data

    def take_action(self, parsed_args):
        # TODO: Common Exception Handling Here
        results = self.execute(parsed_args)
        return self.post_execute(results)


class ListCommand(Command, Lister):
    def post_execute(self, results):
        if len(results) > 0:
            columns = utils.get_columns(results)
            data = [utils.get_item_properties(i, columns) for i in results]
            return columns, data
        else:
            return [], ()


class GetCommand(Command, ShowOne):
    def post_execute(self, results):
        return results.keys(), results.values()


class CreateCommand(Command, ShowOne):
    def post_execute(self, results):
        return results.keys(), results.values()


class UpdateCommand(Command, ShowOne):
    def post_execute(self, results):
        return results.keys(), results.values()


class DeleteCommand(Command):
    pass
