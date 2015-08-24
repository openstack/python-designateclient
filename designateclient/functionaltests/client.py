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


class ZoneCommands(object):
    """This is a mixin that provides zone commands to DesignateCLI"""

    def zone_list(self, *args, **kwargs):
        return self.parsed_cmd('zone list', ListModel, *args, **kwargs)

    def zone_show(self, id, *args, **kwargs):
        return self.parsed_cmd('zone show %s' % id, FieldValueModel, *args,
                               **kwargs)

    def zone_delete(self, id, *args, **kwargs):
        return self.parsed_cmd('zone delete %s' % id, *args, **kwargs)

    def zone_create(self, name, email, *args, **kwargs):
        cmd = 'zone create %s --email %s' % (name, email)
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)


class DesignateCLI(base.CLIClient, ZoneCommands):

    @classmethod
    def get_clients(cls):
        return {
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
