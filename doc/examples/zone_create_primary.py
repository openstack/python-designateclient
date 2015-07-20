from __future__ import print_function

import logging

from designateclient import exceptions
from designateclient import shell
from designateclient.v2 import client

from keystoneclient.auth.identity import generic
from keystoneclient import session as keystone_session


logging.basicConfig(level='DEBUG')

auth = generic.Password(
    auth_url=shell.env('OS_AUTH_URL'),
    username=shell.env('OS_USERNAME'),
    password=shell.env('OS_PASSWORD'),
    tenant_name=shell.env('OS_TENANT_NAME'))

session = keystone_session.Session(auth=auth)

client = client.Client(session=session)


try:
    zone = client.zones.create('i.io.', email='i@i.io')
except exceptions.RemoteError:
    zone = dict([(z['name'], z) for z in client.zones.list()])['i.io.']

print(client.recordsets.list(zone['id']))
