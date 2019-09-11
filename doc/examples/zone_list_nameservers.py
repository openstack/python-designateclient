import logging
import os
import uuid

from designateclient.v2 import client

from keystoneauth1.identity import generic
from keystoneauth1 import session as keystone_session


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

zone = client.zones.create(
    'primary-%s.io.' % str(uuid.uuid4()),
    'PRIMARY',
    'root@x.com')

client.nameservers.list(zone['id'])
