.. _bindings:

===========================
Python Bindings - v2
===========================

The python-designateclient package comes with python bindings
the Designate API: v2. This can be used to interact with the Designate
API from any python program.

Introduction - Bindings v2
==========================

To view examples of usage please checkout the *doc/examples* folder, basic usage is:

.. code-block:: python

   #!/usr/bin/env python
   from designateclient.v2 import client
   from designateclient import shell

   from keystoneauth1.identity import generic
   from keystoneauth1 import session as keystone_session


   auth = generic.Password(
    auth_url=shell.env('OS_AUTH_URL'),
    username=shell.env('OS_USERNAME'),
    password=shell.env('OS_PASSWORD'),
    project_name=shell.env('OS_PROJECT_NAME'),
    project_domain_id='default',
    user_domain_id='default')

   session = keystone_session.Session(auth=auth)

   client = client.Client(session=session)

   zone = client.zones.create('i.io.', email='i@i.io')

   rs = client.recordsets.create(zone['id'], 'www', 'A', ['10.0.0.1'])
