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
import os

from tempest.lib.cli import base

from designateclient.functionaltests.config import cfg
from designateclient.functionaltests.models import FieldValueModel
from designateclient.functionaltests.models import ListModel


LOG = logging.getLogger(__name__)


def build_option_string(options):
    """Format a string of option flags (--key 'value').

    This will quote the values, in case spaces are included.
    Any values that are None are excluded entirely.

    Usage::

        build_option_string({
            "--email": "me@example.com",
            "--name": "example.com."
            "--ttl": None,

        })

    Returns::

        "--email 'me@example.com' --name 'example.com.'
    """
    return " ".join(f"{flag} '{value}'"
                    for flag, value in options.items()
                    if value is not None)


def build_flags_string(flags):
    """Format a string of value-less flags.

    Pass in a dictionary mapping flags to booleans. Those flags set to true
    are included in the returned string.

    Usage::

        build_flags_string({
            '--no-ttl': True,
            '--no-name': False,
            '--verbose': True,
        })

    Returns::

        '--no-ttl --verbose'
    """
    flags = {flag: is_set for flag, is_set in flags.items() if is_set}
    return " ".join(flags.keys())


class ZoneCommands:
    """This is a mixin that provides zone commands to DesignateCLI"""

    def zone_list(self, *args, **kwargs):
        return self.parsed_cmd('zone list', ListModel, *args, **kwargs)

    def zone_show(self, id, *args, **kwargs):
        return self.parsed_cmd(f'zone show {id}', FieldValueModel, *args,
                               **kwargs)

    def zone_delete(self, id, *args, **kwargs):
        return self.parsed_cmd(f'zone delete {id}', FieldValueModel, *args,
                               **kwargs)

    def zone_create(self, name, email=None, ttl=None, description=None,
                    type=None, masters=None, *args, **kwargs):
        options_str = build_option_string({
            "--email": email,
            "--ttl": ttl,
            "--description": description,
            "--masters": masters,
            "--type": type,
        })
        cmd = f'zone create {name} {options_str}'
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
        cmd = f'zone set {id} {options_str}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)


class ZoneTransferCommands:
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
        cmd = f'zone transfer request create {zone_id} {options_str}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def zone_transfer_request_show(self, id, *args, **kwargs):
        cmd = f'zone transfer request show {id}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def zone_transfer_request_set(self, id, description=None, *args, **kwargs):
        options_str = build_option_string({"--description": description})
        cmd = f'zone transfer request set {options_str} {id}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def zone_transfer_request_delete(self, id, *args, **kwargs):
        cmd = f'zone transfer request delete {id}'
        return self.parsed_cmd(cmd, *args, **kwargs)

    def zone_transfer_accept_request(self, id, key, *args, **kwargs):
        options_str = build_option_string({
            "--transfer-id": id,
            "--key": key,
        })
        cmd = f'zone transfer accept request {options_str}'
        return self.parsed_cmd(cmd, *args, **kwargs)

    def zone_transfer_accept_show(self, id, *args, **kwargs):
        cmd = f'zone transfer accept show {id}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def zone_transfer_accept_list(self, *args, **kwargs):
        cmd = 'zone transfer accept list'
        return self.parsed_cmd(cmd, ListModel, *args, **kwargs)


class ZoneExportCommands:
    """A mixin for DesignateCLI to add zone export commands"""

    def zone_export_list(self, *args, **kwargs):
        cmd = 'zone export list'
        return self.parsed_cmd(cmd, ListModel, *args, **kwargs)

    def zone_export_create(self, zone_id, *args, **kwargs):
        cmd = f'zone export create {zone_id}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def zone_export_show(self, zone_export_id, *args, **kwargs):
        cmd = f'zone export show {zone_export_id}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def zone_export_delete(self, zone_export_id, *args, **kwargs):
        cmd = f'zone export delete {zone_export_id}'
        return self.parsed_cmd(cmd, *args, **kwargs)

    def zone_export_showfile(self, zone_export_id, *args, **kwargs):
        cmd = f'zone export showfile {zone_export_id}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)


class ZoneImportCommands:
    """A mixin for DesignateCLI to add zone import commands"""

    def zone_import_list(self, *args, **kwargs):
        cmd = 'zone import list'
        return self.parsed_cmd(cmd, ListModel, *args, **kwargs)

    def zone_import_create(self, zone_file_path, *args, **kwargs):
        cmd = f'zone import create {zone_file_path}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def zone_import_show(self, zone_import_id, *args, **kwargs):
        cmd = f'zone import show {zone_import_id}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def zone_import_delete(self, zone_import_id, *args, **kwargs):
        cmd = f'zone import delete {zone_import_id}'
        return self.parsed_cmd(cmd, *args, **kwargs)


class RecordsetCommands:

    def recordset_show(self, zone_id, id, *args, **kwargs):
        cmd = f'recordset show {zone_id} {id}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def recordset_list(self, zone_id, *args, **kwargs):
        cmd = f'recordset list {zone_id}'
        return self.parsed_cmd(cmd, ListModel, *args, **kwargs)

    def recordset_create(self, zone_id, name, record=None, type=None,
                         description=None, ttl=None, *args, **kwargs):
        options_str = build_option_string({
            # NOTE(tkajinam): --record argument should be repeated when
            # multiple records are used. This code needs update when multiple
            # records are used in functional tests.
            '--record': record,
            '--type': type,
            '--description': description,
            '--ttl': ttl,
        })
        cmd = f'recordset create {zone_id} {name} {options_str}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def recordset_set(self, zone_id, id, record=None, type=None,
                      description=None, ttl=None, no_description=False,
                      no_ttl=False, *args, **kwargs):
        options_str = build_option_string({
            # NOTE(tkajinam): --record argument should be repeated when
            # multiple records are used. This code needs update when multiple
            # records are used in functional tests.
            '--record': record,
            '--type': type,
            '--description': description,
            '--ttl': ttl,
        })
        flags_str = build_flags_string({
            '--no-description': no_description,
            '--no-ttl': no_ttl,
        })
        cmd = f'recordset set {zone_id} {id} {flags_str} {options_str}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def recordset_delete(self, zone_id, id, *args, **kwargs):
        cmd = f'recordset delete {zone_id} {id}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)


class TLDCommands:

    def tld_list(self, *args, **kwargs):
        return self.parsed_cmd('tld list', ListModel, *args, **kwargs)

    def tld_show(self, id, *args, **kwargs):
        return self.parsed_cmd(f'tld show {id}', FieldValueModel,
                               *args, **kwargs)

    def tld_delete(self, id, *args, **kwargs):
        return self.parsed_cmd(f'tld delete {id}', *args, **kwargs)

    def tld_create(self, name, description=None, *args, **kwargs):
        options_str = build_option_string({
            '--name': name,
            '--description': description,
        })
        cmd = f'tld create {options_str}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def tld_set(self, id, name=None, description=None, no_description=False,
                *args, **kwargs):
        options_str = build_option_string({
            '--name': name,
            '--description': description,
        })
        flags_str = build_flags_string({'--no-description': no_description})
        cmd = f'tld set {id} {options_str} {flags_str}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)


class TSIGKeyCommands:
    def tsigkey_list(self, *args, **kwargs):
        return self.parsed_cmd('tsigkey list', ListModel, *args, **kwargs)

    def tsigkey_show(self, id, *args, **kwargs):
        return self.parsed_cmd(f'tsigkey show {id}', FieldValueModel,
                               *args, **kwargs)

    def tsigkey_delete(self, id, *args, **kwargs):
        return self.parsed_cmd(f'tsigkey delete {id}', *args,
                               **kwargs)

    def tsigkey_create(self, name, algorithm, secret, scope, resource_id,
                       *args, **kwargs):
        options_str = build_option_string({
            '--name': name,
            '--algorithm': algorithm,
            '--secret': secret,
            '--scope': scope,
            '--resource-id': resource_id,
        })
        cmd = f'tsigkey create {options_str}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def tsigkey_set(self, id, name=None, algorithm=None, secret=None,
                    scope=None,
                    *args, **kwargs):
        options_str = build_option_string({
            '--name': name,
            '--algorithm': algorithm,
            '--secret': secret,
            '--scope': scope,
        })
        cmd = f'tsigkey set {id} {options_str}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)


class BlacklistCommands:
    def zone_blacklist_list(self, *args, **kwargs):
        cmd = 'zone blacklist list'
        return self.parsed_cmd(cmd, ListModel, *args, **kwargs)

    def zone_blacklist_create(self, pattern, description=None, *args,
                              **kwargs):
        options_str = build_option_string({
            '--pattern': pattern,
            '--description': description,
        })
        cmd = f'zone blacklist create {options_str}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def zone_blacklist_set(self, id, pattern=None, description=None,
                           no_description=False, *args, **kwargs):
        options_str = build_option_string({
            '--pattern': pattern,
            '--description': description,
        })
        flags_str = build_flags_string({'--no-description': no_description})
        cmd = f'zone blacklist set {id} {options_str} {flags_str}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def zone_blacklist_show(self, id, *args, **kwargs):
        cmd = f'zone blacklist show {id}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def zone_blacklist_delete(self, id, *args, **kwargs):
        cmd = f'zone blacklist delete {id}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)


class SharedZoneCommands:

    def shared_zone_show(self, zone_id, shared_zone_id, *args, **kwargs):
        cmd = f'zone share show {zone_id} {shared_zone_id}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def shared_zone_list(self, zone_id, *args, **kwargs):
        cmd = f'zone share list {zone_id}'
        return self.parsed_cmd(cmd, ListModel, *args, **kwargs)

    def share_zone(self, zone_id, target_project_id, *args, **kwargs):
        cmd = f'zone share create {zone_id} {target_project_id}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)

    def unshare_zone(self, zone_id, shared_zone_id, *args, **kwargs):
        cmd = f'zone share delete {zone_id} {shared_zone_id}'
        return self.parsed_cmd(cmd, FieldValueModel, *args, **kwargs)


class DesignateCLI(base.CLIClient, ZoneCommands, ZoneTransferCommands,
                   ZoneExportCommands, ZoneImportCommands, RecordsetCommands,
                   TLDCommands, BlacklistCommands, SharedZoneCommands):

    # instantiate this once to minimize requests to keystone
    _CLIENTS = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # grab the project id. this is used for zone transfer requests
        resp = FieldValueModel(self.openstack('token issue'))
        self.project_id = resp.project_id

    @property
    def using_auth_override(self):
        return bool(cfg.CONF.identity.override_endpoint)

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
        raise Exception(f"User '{user}' does not exist")

    def parsed_cmd(self, cmd, model=None, *args, **kwargs):
        if self.using_auth_override:
            # use --os-url and --os-token
            func = self._openstack_noauth
        else:
            # use --os-username --os-tenant-name --os-password --os-auth-url
            func = self.openstack

        out = func(cmd, *args, **kwargs)
        LOG.debug(out)
        if model is not None:
            return model(out)
        return out

    def _openstack_noauth(self, cmd, *args, **kwargs):
        exe = os.path.join(cfg.CONF.designateclient.directory, 'openstack')
        options = build_option_string({
            '--os-url': cfg.CONF.identity.override_endpoint,
            '--os-token': cfg.CONF.identity.override_token,
        })
        cmd = options + " " + cmd
        return base.execute(exe, cmd, *args, **kwargs)
