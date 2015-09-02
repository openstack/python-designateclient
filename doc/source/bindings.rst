===============
Python Bindings
===============

The python-designateclient package comes with python bindings for the Designate
API. This can be used to interact with the Designate API from any python
program.

Introduction - Bindings v2
==========================

To view examples of usage please checkout the *doc/examples* folder, basic usage is:

.. code-block:: python

   #!/usr/bin/env python
   from designateclient.v2 import client
   from designateclient import shell

   from keystoneclient.auth.identity import generic
   from keystoneclient import session as keystone_session

   auth = generic.Password(
    auth_url=shell.env('OS_AUTH_URL'),
    username=shell.env('OS_USERNAME'),
    password=shell.env('OS_PASSWORD'),
    tenant_name=shell.env('OS_TENANT_NAME'))

   session = keystone_session.Session(auth=auth)

   client = client.Client(session=session)

   zone = client.zones.create('i.io.', email='i@i.io')

   rs = client.recordsets.create(zone['id'], 'www', 'A', ['10.0.0.1'])

Introduction
============

Below is a simple example of how to instantiate and perform basic tasks using
the bindings.

.. code-block:: python

   #!/usr/bin/env python
   from __future__ import print_function
   from designateclient.v1 import Client

   # Create an instance of the client, providing the necessary credentials
   client = Client(
       auth_url="https://example.com:5000/v2.0/",
       username="openstack",
       password="yadayada",
       tenant_id="123456789"
   )

   # Fetch a list of the domains this user/tenant has access to
   domains = client.domains.list()

   # Iterate the list, printing some useful information
   for domain in domains:
       print("Domain ID: %s, Name: %s" % (domain.id, domain.name))

And the output this program might produce:

.. code-block:: console

   $ python /tmp/example.py
   Domain ID: 467f97b4-f074-4839-ae85-1a61fccfb83d, Name: example-one.com.
   Domain ID: 6d3bf479-8a93-47ae-8c65-3dff8dba1b0d, Name: example-two.com.


Authentication
==============

Designate supports either Keystone authentication, or no authentication at all.

Keystone Authentication
-----------------------

Below is a sample of standard authentication with keystone:

.. code-block:: python

   #!/usr/bin/env python

   from designateclient.v1 import Client

   # Create an instance of the client, providing the necessary credentials
   client = Client(
       auth_url="https://example.com:5000/v2.0/",
       username="openstack",
       password="yadayada",
       tenant_id="123456789"
   )

Below is a sample of standard authentication with keystone, but also explicitly
providing the endpoint to use:

.. note:: This is useful when a development Designate instances authenticates
          against a production Keystone.

.. code-block:: python

   #!/usr/bin/env python

   from designateclient.v1 import Client

   # Create an instance of the client, providing the necessary credentials
   client = Client(
       auth_url="https://example.com:5000/v2.0/",
       username="openstack",
       password="yadayada",
       tenant_id="123456789",
       endpoint="https://127.0.0.1:9001/v1/"
   )

No Authentication
-----------------

Below is a sample of interaction with a non authenticated designate:

.. code-block:: python

   #!/usr/bin/env python

   from designateclient.v1 import Client

   # Create an instance of the client, providing the endpoint directly
   client = Client(
       endpoint="https://127.0.0.1:9001/v1/"
   )

Working with Domains
====================

The Domain Object
-----------------

Object Properties:

======================= =======================================================
Property                Description
======================= =======================================================
id                      Domain ID
name                    Domain Name (e.g. example.com.)
email                   Domain Responsible Person Email (e.g. fred@example.com)
ttl                     Default TTL for records
serial                  Domain Server Number
created_at              Date and time this domain was created at
updated_at              Date and time this domain was last updated
description             Domain Description
======================= =======================================================

Listing Domains
---------------

.. code-block:: python

   #!/usr/bin/env python

   from designateclient.v1 import Client

   # Create an instance of the client
   client = Client(
       endpoint="https://127.0.0.1:9001/v1/"
   )

   # List All Domains
   domains = client.domains.list()

Fetching a Domain by ID
-----------------------

.. code-block:: python

   #!/usr/bin/env python

   from designateclient.v1 import Client

   # Create an instance of the client
   client = Client(
       endpoint="https://127.0.0.1:9001/v1/"
   )

   domain_id = 'fb505f10-25df-11e3-8224-0800200c9a66'

   # Fetch the domain
   domain = client.domains.get(domain_id)


Creating a Domain
-----------------

.. code-block:: python

   #!/usr/bin/env python

   from designateclient.v1 import Client
   from designateclient.v1.domains import Domain

   # Create an instance of the client
   client = Client(
       endpoint="https://127.0.0.1:9001/v1/"
   )

   # Create a new Domain object
   domain = Domain(name="example.com.", email="fred@example.com")

   # Send the Create Domain API call
   domain = client.domains.create(domain)

Updating a Domain
-----------------

.. code-block:: python

   #!/usr/bin/env python

   from designateclient.v1 import Client

   # Create an instance of the client
   client = Client(
       endpoint="https://127.0.0.1:9001/v1/"
   )

   domain_id = 'fb505f10-25df-11e3-8224-0800200c9a66'

   # Fetch the domain
   domain = client.domains.get(domain_id)

   # Update a value on the Domain
   domain.ttl = 300

   # Send the Update Domain API call
   domain = client.domains.update(domain)

Deleting a Domain
-----------------

.. code-block:: python

   #!/usr/bin/env python

   from designateclient.v1 import Client

   # Create an instance of the client
   client = Client(
       endpoint="https://127.0.0.1:9001/v1/"
   )

   domain_id = 'fb505f10-25df-11e3-8224-0800200c9a66'

   # Fetch the domain
   domains = client.domains.delete(domain_id)

Working with Records
====================

The Record Object
-----------------

Object Properties:

======================= =======================================================
Property                Description
======================= =======================================================
id                      Record ID
domain_id               Domain ID
name                    Record Name (e.g. example.com.)
type                    Record Type (e.g. A, AAAA, CNAME, MX, SRV etc)
data                    Record Data (e.g. 127.0.0.1)
priority                Rercord Priority (Valid only for MX and SRV records)
ttl                     Record TTL
created_at              Date and time this record was created at
updated_at              Date and time this record was last updated
description             Record Description
======================= =======================================================

Listing Records
---------------

.. code-block:: python

   #!/usr/bin/env python

   from designateclient.v1 import Client

   # Create an instance of the client
   client = Client(
       endpoint="https://127.0.0.1:9001/v1/"
   )

   domain_id = 'fb505f10-25df-11e3-8224-0800200c9a66'

   # List All Records
   records = client.records.list(domain_id)

Fetching a Record by ID
-----------------------

.. code-block:: python

   #!/usr/bin/env python

   from designateclient.v1 import Client

   # Create an instance of the client
   client = Client(
       endpoint="https://127.0.0.1:9001/v1/"
   )

   domain_id = 'fb505f10-25df-11e3-8224-0800200c9a66'
   record_id = 'bd3e8520-25e0-11e3-8224-0800200c9a66'

   # Fetch the record
   records = client.records.get(domain_id, record_id)


Creating a Record
-----------------

.. code-block:: python

   #!/usr/bin/env python

   from designateclient.v1 import Client
   from designateclient.v1.records import Record

   # Create an instance of the client
   client = Client(
       endpoint="https://127.0.0.1:9001/v1/"
   )

   domain_id = 'fb505f10-25df-11e3-8224-0800200c9a66'

   # Create a new Record object
   record = Record(name="www.example.com.", type="A", data="127.0.0.1")

   # Send the Create Record API call
   record = client.records.create(domain_id, record)

Updating a Record
-----------------

.. code-block:: python

   #!/usr/bin/env python

   from designateclient.v1 import Client

   # Create an instance of the client
   client = Client(
       endpoint="https://127.0.0.1:9001/v1/"
   )

   domain_id = 'fb505f10-25df-11e3-8224-0800200c9a66'
   record_id = 'bd3e8520-25e0-11e3-8224-0800200c9a66'

   # Fetch the record
   record = client.records.get(record_id)

   # Update a value on the Record
   record.ttl = 300

   # Send the Update Record API call
   record = client.records.update(domain_id, record)

Deleting a Record
-----------------

.. code-block:: python

   #!/usr/bin/env python

   from designateclient.v1 import Client

   # Create an instance of the client
   client = Client(
       endpoint="https://127.0.0.1:9001/v1/"
   )

   domain_id = 'fb505f10-25df-11e3-8224-0800200c9a66'
   record_id = 'bd3e8520-25e0-11e3-8224-0800200c9a66'

   # Fetch the record
   records = client.records.delete(domain_id, record_id)

Working with Servers
====================

The Server Object
-----------------

Object Properties:

======================= =======================================================
Property                Description
======================= =======================================================
id                      Server ID
name                    Server Name (e.g. example.com.)
created_at              Date and time this server was created at
updated_at              Date and time this server was last updated
======================= =======================================================

Listing Servers
---------------

.. code-block:: python

   #!/usr/bin/env python

   from designateclient.v1 import Client

   # Create an instance of the client
   client = Client(
       endpoint="https://127.0.0.1:9001/v1/"
   )

   # List All Servers
   servers = client.servers.list()

Fetching a Server by ID
-----------------------

.. code-block:: python

   #!/usr/bin/env python

   from designateclient.v1 import Client

   # Create an instance of the client
   client = Client(
       endpoint="https://127.0.0.1:9001/v1/"
   )

   server_id = 'fb505f10-25df-11e3-8224-0800200c9a66'

   # Fetch the server
   server = client.servers.get(server_id)


Creating a Server
-----------------

.. code-block:: python

   #!/usr/bin/env python

   from designateclient.v1 import Client
   from designateclient.v1.servers import Server

   # Create an instance of the client
   client = Client(
       endpoint="https://127.0.0.1:9001/v1/"
   )

   # Create a new Server object
   server = Server(name="ns1.example.com.")

   # Send the Create Server API call
   server = client.servers.create(server)

Updating a Server
-----------------

.. code-block:: python

   #!/usr/bin/env python

   from designateclient.v1 import Client

   # Create an instance of the client
   client = Client(
       endpoint="https://127.0.0.1:9001/v1/"
   )

   server_id = 'fb505f10-25df-11e3-8224-0800200c9a66'

   # Fetch the server
   server = client.servers.get(server_id)

   # Update a value on the Server
   server.name = "ns2.example.com"

   # Send the Update Server API call
   server = client.servers.update(server)

Deleting a Server
-----------------

.. code-block:: python

   #!/usr/bin/env python

   from designateclient.v1 import Client

   # Create an instance of the client
   client = Client(
       endpoint="https://127.0.0.1:9001/v1/"
   )

   server_id = 'fb505f10-25df-11e3-8224-0800200c9a66'

   # Fetch the server
   servers = client.servers.delete(server_id)
