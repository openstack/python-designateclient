================
Functional Tests
================

The functional tests invoke the client executable to see that it actually works
with a running Designate. WARNING: these tests will create and delete zones,
recordsets, and other resources in Designate.

Installation
------------

.. code-block:: shell-session

    cd python-designateclient
    pip install python-openstackclient
    pip install -r requirements.txt -r test-requirements.txt
    pip install -e .

Configuration
-------------

The functional tests look for a variable ``TEMPEST_CONFIG`` which specifies a
config file for the test.

.. code-block:: shell-session

    export TEMPEST_CONFIG=tempest.conf

The tests will use Keystone to grab the Designate endpoint to test against.
They need at least three users (two regular users, and one admin) for all the
tests to run.

.. code-block:: shell-session

    [identity]
    uri = http://localhost:5000/v2.0
    uri_v3 = http://localhost:5000/v3
    auth_version = v2
    region = RegionOne

    username = demo
    tenant_name = demo
    password = password
    domain_name = Default

    alt_username = alt_demo
    alt_tenant_name = alt_demo
    alt_password = password
    alt_domain_name = Default

    admin_username = admin
    admin_tenant_name = admin
    admin_password = password
    admin_domain_name = Default

    [designateclient]
    # the directory containing the openstack executable
    directory=/root/python-designateclient/.venv/bin

Running the tests
-----------------

The functional tests are run with tox (installed with ``pip install tox``):

.. code-block:: shell-session

    tox -e functional
