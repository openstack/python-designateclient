from __future__ import print_function
import logging

from keystoneclient.auth.identity import generic
from keystoneclient import session as keystone_session

from designateclient import shell
from designateclient.v2 import client

logging.basicConfig(level='DEBUG')

auth = generic.Password(
    auth_url=shell.env('OS_AUTH_URL'),
    username=shell.env('OS_USERNAME'),
    password=shell.env('OS_PASSWORD'),
    tenant_name=shell.env('OS_TENANT_NAME'))

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
