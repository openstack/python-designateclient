import logging
import uuid

from designateclient.v2 import client
from designateclient import shell
from designateclient import utils

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

zone = client.zones.create(
    'primary-%s.io.' % str(uuid.uuid4()),
    'PRIMARY',
    'root@x.com')

client.nameservers.list(zone['id'])
