======================================
designate command line tool - examples
======================================

Using the client against your dev environment
---------------------------------------------
Typically the designate client talks to Keystone (or a Keystone like service) via the OS_AUTH_URL setting & retrives the designate endpoint from the returned service catalog.  Using ``--os-endpoint`` or ``OS_ENDPOINT`` you can specify the end point directly, this is useful if you want to point the client at a test environment that's running without a full Keystone service.

.. code-block:: shell-session

    $ designate --os-endpoint http://127.0.0.1:9001/v1 server-create --name ns.foo.com.
    +------------+--------------------------------------+
    | Field      | Value                                |
    +------------+--------------------------------------+
    | id         | 3dee78df-c6b8-4fbd-8e89-3186c1a4734f |
    | created_at | 2015-11-04T08:47:12.000000           |
    | updated_at | None                                 |
    | name       | ns.foo.com.                          |
    +------------+--------------------------------------+

    $ designate --os-endpoint http://127.0.0.1:9001/v1 domain-create --name testing123.net. --email me@mydomain.com
    +-------------+--------------------------------------+
    | Field       | Value                                |
    +-------------+--------------------------------------+
    | description | None                                 |
    | created_at  | 2015-11-04T08:49:53.000000           |
    | updated_at  | None                                 |
    | email       | me@mydomain.com                      |
    | ttl         | 3600                                 |
    | serial      | 1446626993                           |
    | id          | f98c3d91-f514-4956-a955-20eefb413a64 |
    | name        | testing123.net.                      |
    +-------------+--------------------------------------+

    $ designate --os-endpoint http://127.0.0.1:9001/v1 record-create --name myhost.testing123.net. --type A --data 1.2.3.4 f98c3d91-f514-4956-a955-20eefb413a64
    +-------------+--------------------------------------+
    | Field       | Value                                |
    +-------------+--------------------------------------+
    | description | None                                 |
    | type        | A                                    |
    | created_at  | 2015-11-04T08:52:41.000000           |
    | updated_at  | None                                 |
    | domain_id   | f98c3d91-f514-4956-a955-20eefb413a64 |
    | priority    | None                                 |
    | ttl         | None                                 |
    | data        | 1.2.3.4                              |
    | id          | b5a74471-8062-4395-be70-968805a0d832 |
    | name        | myhost.testing123.net.               |
    +-------------+--------------------------------------+

