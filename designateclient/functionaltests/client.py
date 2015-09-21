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
import logging

from tempest_lib.cli import base

from designateclient.functionaltests.config import cfg
from designateclient.functionaltests.models import FieldValueModel
from designateclient.functionaltests.models import ListModel


LOG = logging.getLogger(__name__)


def build_option_string(options):
    """Format a string of option flags (--key 'value').

    This will quote the values, in case spaces are included.
    Any values that are None are excluded entirely.

    Usage:
        build_option_string({
            "--email": "me@example.com",
            "--name": "example.com."
            "--ttl": None,

        })

    Returns:
        "--email 'me@example.com' --name 'example.com.'
    """
    return " ".join("{0} '{1}'".format(flag, value)
                    for flag, value in options.items()
                    if value is not None)


class ZoneCommands(object):
    """This is a mixin that provides zone commands to DesignateCLI"""

    def zone_list(self, *args, **kwargs):
        return self.parsed_cmd('zone list', ListModel, *args, **kwargs)

    def zone_show(self, id, *args, **kwargs):
        return self.parsed_cmd('zone show %s' % id, FieldValueModel, *args,
                               **kwargs)

    def zone_delete(self, id, *args, **kwargs):
        return self.parsed_cmd('zone delete %s' % id, *args, **kwargs)

    def zone_create(self, name, email=None, ttl=None, description=None,
                    type=None, masters=None, *args, **kwargs):
        options_str = build_option_string({
            "--email": email,
            "--ttl": ttl,
            "--description": description,
            "--masters": masters,
            "--type": type,
        })
        cmd = 'zone create {0} {1}'.format(name, options_str)
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def zone_set(self, id, email=None, ttl=None, description=None,
                 type=None, masters=None, *args, **kwargs):
        options_str = build_option_string({
            "--email": email,
            "--ttl": ttl,
            "--description": description,
            "--masters": masters,
            "--type": type,
        })
        cmd = 'zone set {0} {1}'.format(id, options_str)
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)


class ZoneTransferCommands(object):
    """A mixin for DesignateCLI to add zone transfer commands"""

    def zone_transfer_request_list(self, *args, **kwargs):
        cmd = 'zone transfer request list'
        return self.parsed_cmd(cmd, ListModel, *args, **kwargs)

    def zone_transfer_request_create(self, zone_id, target_project_id=None,
                                     description=None, *args, **kwargs):
        options_str = build_option_string({
            "--target-project-id": target_project_id,
            "--description": description,
        })
        cmd = 'zone transfer request create {0} {1}'.format(
            zone_id, options_str)
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def zone_transfer_request_show(self, id, *args, **kwargs):
        cmd = 'zone transfer request show {0}'.format(id)
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def zone_transfer_request_set(self, id, description=None, *args, **kwargs):
        options_str = build_option_string({"--description": description})
        cmd = 'zone transfer request set {0} {1}'.format(options_str, id)
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def zone_transfer_request_delete(self, id, *args, **kwargs):
        cmd = 'zone transfer request delete {0}'.format(id)
        return self.parsed_cmd(cmd, *args, **kwargs)

    def zone_transfer_accept_request(self, id, key, *args, **kwargs):
        options_str = build_option_string({
            "--transfer-id": id,
            "--key": key,
        })
        cmd = 'zone transfer accept request {0}'.format(options_str)
        return self.parsed_cmd(cmd, *args, **kwargs)

    def zone_transfer_accept_show(self, id, *args, **kwargs):
        cmd = 'zone transfer accept show {0}'.format(id)
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)


class DesignateCLI(base.CLIClient, ZoneCommands, ZoneTransferCommands):

    # instantiate this once to minimize requests to keystone
    _CLIENTS = None

    def __init__(self, *args, **kwargs):
        super(DesignateCLI, self).__init__(*args, **kwargs)
        # grab the project id. this is used for zone transfer requests
        resp = FieldValueModel(self.keystone('token-get'))
        self.project_id = resp.tenant_id

    @classmethod
    def get_clients(cls):
        if not cls._CLIENTS:
            cls._init_clients()
        return cls._CLIENTS

    @classmethod
    def _init_clients(cls):
        cls._CLIENTS = {
            'default': DesignateCLI(
                cli_dir=cfg.CONF.designateclient.directory,
                username=cfg.CONF.identity.username,
                password=cfg.CONF.identity.password,
                tenant_name=cfg.CONF.identity.tenant_name,
                uri=cfg.CONF.identity.uri,
            ),
            'alt': DesignateCLI(
                cli_dir=cfg.CONF.designateclient.directory,
                username=cfg.CONF.identity.alt_username,
                password=cfg.CONF.identity.alt_password,
                tenant_name=cfg.CONF.identity.alt_tenant_name,
                uri=cfg.CONF.identity.uri,
            ),
            'admin': DesignateCLI(
                cli_dir=cfg.CONF.designateclient.directory,
                username=cfg.CONF.identity.admin_username,
                password=cfg.CONF.identity.admin_password,
                tenant_name=cfg.CONF.identity.admin_tenant_name,
                uri=cfg.CONF.identity.uri,
            )
        }

    @classmethod
    def as_user(self, user):
        clients = self.get_clients()
        if user in clients:
            return clients[user]
        raise Exception("User '{0}' does not exist".format(user))

    def parsed_cmd(self, cmd, model=None, *args, **kwargs):
        out = self.openstack(cmd, *args, **kwargs)
        LOG.debug(out)
        if model is not None:
            return model(out)
        return out
