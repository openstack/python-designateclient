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
import six
from tempest_lib.cli import output_parser


class Model(object):

    def __str__(self):
        return str(self.__dict__)


class FieldValueModel(Model):
    """This converts cli output from messy lists/dicts to neat attributes."""

    def __init__(self, out):
        """This parses output with fields and values like:

            +----------------+------------------------------+
            | Field          | Value                        |
            +----------------+------------------------------+
            | action         | CREATE                       |
            | created_at     | 2015-08-20T17:22:17.000000   |
            | description    | None                         |
            +----------------+------------------------------+

        These are then accessible as:

            model.action
            model.created_at
            model.description

        """
        table = output_parser.table(out)
        for field, value in table['values']:
            setattr(self, field, value)


class ListEntryModel(Model):

    def __init__(self, fields, values):
        for k, v in six.moves.zip(fields, values):
            setattr(self, k, v)


class ListModel(Model, list):

    def __init__(self, out):
        """This parses an output table with any number of headers, and any
        number of entries:

            +--------------------------------------+----------+---------+
            | id                                   | name     | type    |
            +--------------------------------------+----------+---------+
            | e658a875-1024-4f88-a347-e5b244ec5a10 | aaa.com. | PRIMARY |
            +--------------------------------------+----------+---------+
            | 98d1fb5f-2954-448e-988e-6f1df0f24c52 | bbb.com. | PRIMARY |
            +--------------------------------------+----------+---------+

        These are then accessible as:

            model[0].name == 'aaa.com.'
            model[1].name == 'bbb.com.'

        """
        table = output_parser.table(out)
        for entry in table['values']:
            self.append(ListEntryModel(table['headers'], entry))
