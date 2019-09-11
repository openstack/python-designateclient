import logging
import os
import uuid

from keystoneauth1.identity import generic
from keystoneauth1 import session as keystone_session

from designateclient.v2 import client


logging.basicConfig(level='DEBUG')

auth = generic.Password(
    auth_url=os.environ.get('OS_AUTH_URL'),
    username=os.environ.get('OS_USERNAME'),
    password=os.environ.get('OS_PASSWORD'),
    project_name=os.environ.get('OS_PROJECT_NAME'),
    project_domain_id='default',
    user_domain_id='default')

session = keystone_session.Session(auth=auth)

client = client.Client(session=session)

# Primary Zone
primary = client.zones.create(
    'primary-%s.io.' % str(uuid.uuid4()),
    'PRIMARY',
    'root@x.com')

# Secondary Zone
slave = client.zones.create(
    'secondary-%s.io.' % str(uuid.uuid4()),
    'SECONDARY',
    masters=["127.0.1.1"])

# Try updating Masters for the Secondary
new_slave = client.zones.update(
    slave['id'],
    {"masters": ["10.0.0.1", "10.0.0.10"]}
)

# List all Zones
zones = client.zones.list()
