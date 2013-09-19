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
    | created_at | 2013-07-09T13:20:23.664811           |
    | id         | 1af2d561-b802-44d7-8208-46475dcd45f9 |
    | name       | ns.foo.com.                          |
    | updated_at | None                                 |
    +------------+--------------------------------------+

    $ designate --os-endpoint http://127.0.0.1:9001/v1 domain-create --name testing123.net. --email simon@mccartney.ie
    +------------+--------------------------------------+
    | Field      | Value                                |
    +------------+--------------------------------------+
    | name       | testing123.net.                      |
    | created_at | 2013-07-09T13:20:30.826155           |
    | updated_at | None                                 |
    | id         | 5c02c519-4928-4a38-bd10-c748c200912f |
    | ttl        | 3600                                 |
    | serial     | 1373376030                           |
    | email      | simon@mccartney.ie                   |
    +------------+--------------------------------------+

    $ designate --os-endpoint http://127.0.0.1:9001/v1 record-create --name myhost.testing123.net. --type A --data 1.2.3.4 5c02c519-4928-4a38-bd10-c748c200912f
