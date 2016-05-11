from __future__ import print_function
import logging

from designateclient.v2 import client
from designateclient import exceptions
from designateclient import shell

from keystoneauth1.identity import generic
from keystoneauth1 import session as keystone_session


logging.basicConfig(level='DEBUG')

"""
Example script to create or get a domain and add some records to it.
"""


auth = generic.Password(
    auth_url=shell.env('OS_AUTH_URL'),
    username=shell.env('OS_USERNAME'),
    password=shell.env('OS_PASSWORD'),
    project_name=shell.env('OS_PROJECT_NAME'),
    project_domain_id='default',
    user_domain_id='default')

session = keystone_session.Session(auth=auth)

client = client.Client(session=session)


try:
    zone = client.zones.create('i.io.', email='i@i.io')
except exceptions.RemoteError:
    zone = dict([(z['name'], z) for z in client.zones.list()])['i.io.']

print("Recordset list...")
for rs in client.recordsets.list(zone['id']):
    print(rs)

# Here's an example of just passing "www" as the record name vs "www.i.io."
records = ["10.0.0.1"]
rs = client.recordsets.create(zone['id'], 'www', 'A', records)

# Here we're replacing the records with new ones
records = ["10.0.0.1", "10.0.0.5"]
client.recordsets.update(zone['id'], rs['id'], {'records': records})
