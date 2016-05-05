====================================
Designate Command Line Tool Examples
====================================

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

    $ designate --os-endpoint http://127.0.0.1:9001/v1 record-create --name myhost.testing123.net. --type A --data 1.2.3.4 f98c3d91-f514-4956-a955-20eefb413a64 (domain_id)
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

    $ designate domain-list
    +--------------------------------------+-------------+------------+
    | id                                   | name        |     serial |
    +--------------------------------------+-------------+------------+
    | 88c14ecf-b034-424c-b081-ca42494dcdf9 | sample.com. | 1462372104 |
    +--------------------------------------+-------------+------------+

    $ designate domain-update --email sample@example.com 88c14ecf-b034-424c-b081-ca42494dcdf9 (domain_id)
    +-------------+--------------------------------------+
    | Field       | Value                                |
    +-------------+--------------------------------------+
    | description | None                                 |
    | created_at  | 2016-05-04T14:28:24.000000           |
    | updated_at  | 2016-05-04T14:29:48.000000           |
    | email       | sample@example.com                   |
    | ttl         | 3600                                 |
    | serial      | 1462372188                           |
    | id          | 88c14ecf-b034-424c-b081-ca42494dcdf9 |
    | name        | sample.com.                          |
    +-------------+--------------------------------------+

    $ designate domain-delete 88c14ecf-b034-424c-b081-ca42494dcdf9 (domain_id)

    $ designate record-list 66584cdd-f7a6-4f0e-acf0-3dd5ad04830d (domain_id)
    +--------------------------------------+------+-----------------------+-----------------------------------------------------------------+
    | id                                   | type | name                  | data                                                            |
    +--------------------------------------+------+-----------------------+-----------------------------------------------------------------+
    | fdfab9c3-51c0-42b9-b500-7779ef917915 | SOA  | example.com.          | ns1.example.org. pr8721.att.com. 1462372695 3600 600 86400 3600 |
    | 242a16e8-8455-4b4d-af7f-45de1074aa04 | NS   | example.com.          | xyz.com.                                                        |
    | 8dc14df7-3651-49df-8c83-0d71954c6152 | NS   | example.com.          | ns1.example.org.                                                |
    | 7e80531d-bd65-49bc-a316-a6a06cd7fe26 | A    | example1.example.com. | 198.51.100.1                                                     |
    +--------------------------------------+------+-----------------------+-----------------------------------------------------------------+

    $ designate record-update --name example1.example.com. --type A --data 198.5.100.2 --ttl 3600 66584cdd-f7a6-4f0e-acf0-3dd5ad04830d (domain-id) 7e80531d-bd65-49bc-a316-a6a06cd7fe26 (record_id)
    +-------------+--------------------------------------+
    | Field       | Value                                |
    +-------------+--------------------------------------+
    | description | None                                 |
    | type        | A                                    |
    | created_at  | 2016-05-04T14:38:15.000000           |
    | updated_at  | 2016-05-04T16:12:05.000000           |
    | domain_id   | 66584cdd-f7a6-4f0e-acf0-3dd5ad04830d |
    | priority    | None                                 |
    | ttl         | 3600                                 |
    | data        | 198.5.100.2                          |
    | id          | 7e80531d-bd65-49bc-a316-a6a06cd7fe26 |
    | name        | example1.example.com.                |
    +-------------+--------------------------------------+

    $ designate record-delete 66584cdd-f7a6-4f0e-acf0-3dd5ad04830d (domain-id) 7e80531d-bd65-49bc-a316-a6a06cd7fe26 (record_id)

    $ designate server-update --name abc.org. 3d9d220d-d111-436a-b9bb-e7bc0e275803 (server_id)
    +------------+--------------------------------------+
    | Field      | Value                                |
    +------------+--------------------------------------+
    | updated_at | None                                 |
    | created_at | 2016-05-04T16:17:16.000000           |
    | id         | 3d9d220d-d111-436a-b9bb-e7bc0e275803 |
    | name       | abc.org.                             |
    +------------+--------------------------------------+

    $ designate server-list
    +--------------------------------------+------------------+
    | id                                   | name             |
    +--------------------------------------+------------------+
    | 4f6f0cbe-ea38-453e-97c5-091617a06b41 | ns1.example.org. |
    | 326de09b-691e-4e4e-bf1c-5a1bf7e7f44d | xyz.com.         |
    | 3d9d220d-d111-436a-b9bb-e7bc0e275803 | abc.org.         |
    +--------------------------------------+------------------+

    $ designate server-get 3d9d220d-d111-436a-b9bb-e7bc0e275803 (server_id)
    +------------+--------------------------------------+
    | Field      | Value                                |
    +------------+--------------------------------------+
    | updated_at | 2016-05-04T16:18:06.000000           |
    | created_at | 2016-05-04T16:17:16.000000           |
    | id         | 3d9d220d-d111-436a-b9bb-e7bc0e275803 |
    | name       | abc.org.                             |
    +------------+--------------------------------------+

    $ designate server-delete 3d9d220d-d111-436a-b9bb-e7bc0e275803 (server_id)

    $ designate quota-get 70a4596c9974429db5fb6fe240ab87b9 (tenant_id)
    +-------------------+-------+
    | Field             | Value |
    +-------------------+-------+
    | domains           | 10    |
    | domain_recordsets | 500   |
    | recordset_records | 20    |
    | domain_records    | 500   |
    +-------------------+-------+

    $ designate quota-update --domains 50 --domain-recordsets 1000 --recordset-records 40 --domain-records 1000 70a4596c9974429db5fb6fe240ab87b9 (tenant_id)
    +-------------------+-------+
    | Field             | Value |
    +-------------------+-------+
    | domains           | 50    |
    | domain_recordsets | 1000  |
    | recordset_records | 40    |
    | domain_records    | 1000  |
    +-------------------+-------+

    $ designate quota-get 70a4596c9974429db5fb6fe240ab87b9 (tenant_id)
    +-------------------+-------+
    | Field             | Value |
    +-------------------+-------+
    | domains           | 10    |
    | domain_recordsets | 500   |
    | recordset_records | 20    |
    | domain_records    | 500   |
    +-------------------+-------+
