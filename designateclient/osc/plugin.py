# Copyright 2014 Hewlett-Packard Development Company, L.P.
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

from osc_lib import utils as oscutils

from designateclient import shell


DEFAULT_API_VERSION = '2'

API_NAME = 'dns'
API_VERSION_OPTION = 'os_dns_api_version'
API_VERSIONS = {
    '2': 'designateclient.v2.client.Client',
}


def make_client(instance):
    cls = oscutils.get_client_class(
        API_NAME, instance._api_version[API_NAME],
        API_VERSIONS)
    kwargs = oscutils.build_kwargs_dict('endpoint_type', instance._interface)

    parsed_args = instance.get_configuration()

    return cls(session=instance.session,
               region_name=instance._region_name,
               all_projects=parsed_args.get('all_projects', False),
               edit_managed=parsed_args.get('edit_managed', False),
               sudo_project_id=parsed_args.get('sudo_project_id', None),
               **kwargs)


def build_option_parser(parser):
    """Hook to add global options."""
    parser.add_argument(
        '--os-dns-api-version',
        metavar='<dns-api-version>',
        default=shell.env('OS_DNS_API_VERSION', default="2"),
        help='DNS API version, default=' +
             DEFAULT_API_VERSION +
             ' (Env: OS_DNS_API_VERSION)')

    parser.add_argument(
        '--all-projects',
        default=False,
        action='store_true',
        help='Show results from all projects. Default=False')

    parser.add_argument(
        '--edit-managed',
        default=False,
        action='store_true',
        help='Edit resources marked as managed. Default=False')

    parser.add_argument(
        '--sudo-project-id',
        default=None,
        help='Project ID to impersonate for this command. Default=None')

    return parser
