from __future__ import print_function
import logging
import os

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

session = keystone_session.Session(auth=auth, timeout=10)

client = client.Client(session=session)


pages = []

fetch = 1
while fetch:
    kw = {'limit': 3}
    if pages:
        # marker is the latest page with the last item.
        kw['marker'] = pages[-1][-1]['id']
    page = client.zones.list(**kw)
    if not page:
        break
    pages.append(page)

for page in pages:
    print(page)
