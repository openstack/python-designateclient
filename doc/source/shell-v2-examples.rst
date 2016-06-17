====================================
OpenStack Command Line Tool Examples
====================================

Because command output would make this document long, much of it will be
omitted from the examples.

Working with Zones
------------------
Create a zone with the following command:

.. code-block:: shell-session

   $ openstack zone create --email admin@example.com example.com.
   +----------------+--------------------------------------+
   | Field          | Value                                |
   +----------------+--------------------------------------+
   | action         | CREATE                               |
   | created_at     | 2016-04-19T17:44:04.000000           |
   | description    | None                                 |
   | email          | admin@example.com                    |
   | id             | 388814ef-3c5d-415e-a866-5b1d13d78dae |
   | masters        |                                      |
   | name           | example.com.                         |
   | pool_id        | 794ccc2c-d751-44fe-b57f-8894c9f5c842 |
   | project_id     | 123456                               |
   | serial         | 1461087844                           |
   | status         | PENDING                              |
   | transferred_at | None                                 |
   | ttl            | 3600                                 |
   | type           | PRIMARY                              |
   | updated_at     | None                                 |
   | version        | 1                                    |
   +----------------+--------------------------------------+

See the new zone in your list of zones with the following command:

.. code-block:: shell-session

   $ openstack zone list

Display a specific zone with either of these commands; most zone commands
accept either the zone_id or name attribute:

.. code-block:: shell-session

   $ openstack zone show example.com.
   $ openstack zone show 388814ef-3c5d-415e-a866-5b1d13d78dae

Update the zone with this command:

.. code-block:: shell-session

   $ openstack zone set --description "Description" example.com.

Delete the zone with this command:

.. code-block:: shell-session

   $ openstack zone delete example.com.

Working with Recordsets
-----------------------
Using the zone above, create a recordset with the following command:

.. code-block:: shell-session

  $ openstack recordset create example.com. --type A www --records 192.0.2.20
  +-------------+--------------------------------------+
  | Field       | Value                                |
  +-------------+--------------------------------------+
  | action      | CREATE                               |
  | created_at  | 2016-04-19T17:51:12.000000           |
  | description | None                                 |
  | id          | 180d3574-3c29-4ea2-b6ff-df904bd3f126 |
  | name        | www.example.com.                     |
  | records     | 192.0.2.20                           |
  | status      | PENDING                              |
  | ttl         | None                                 |
  | type        | A                                    |
  | updated_at  | None                                 |
  | version     | 1                                    |
  | zone_id     | 388814ef-3c5d-415e-a866-5b1d13d78dae |
  +-------------+--------------------------------------+

Multiple records can be provided for a specific recordset type:

.. code-block:: shell-session

  $ openstack recordset create example.com. --type A www --records 192.0.2.20 192.0.2.21

See the new recordset in the list of recordsets with the following command:

.. code-block:: shell-session

   $ openstack recordset list example.com.

Display a specific recordset:

.. code-block:: shell-session

   $ openstack recordset show example.com. www.example.com.

Update a specific recordset:

.. code-block:: shell-session

   $ openstack recordset set example.com. www.example.com. --ttl 10000 --records 192.0.2.20 192.0.2.21

Delete a recordset:

.. code-block:: shell-session

   $ openstack recordset delete example.com. www.example.com.

Working with PTR Records
------------------------
Reverse DNS for Neutron Floating IPs can be managed with the "ptr" subcommand.

List all PTR records:

.. code-block:: shell-session

   $ openstack ptr record list

Show a PTR record:

.. code-block:: shell-session

   $ openstack ptr record show RegionOne:5c02c519-4928-4a38-bd10-c748c200912f

Create a PTR record:

.. code-block:: shell-session

   $ openstack ptr record set RegionOne:5c02c519-4928-4a38-bd10-c748c200912f mail.example.com.

Delete a PTR record:

.. code-block:: shell-session

   $ openstack ptr record delete RegionOne:5c02c519-4928-4a38-bd10-c748c200912f

Working with Zone Exports
-------------------------
Zone exports enable you to save Designate zone information offline.

Create a zone export:

.. code-block:: shell-session

   $ openstack zone export create example.com.
   +------------+--------------------------------------+
   | Field      | Value                                |
   +------------+--------------------------------------+
   | created_at | 2016-04-19T20:42:16.000000           |
   | id         | 6d5acb9d-f3d6-4ed4-96e1-03bc0e405bb5 |
   | location   | None                                 |
   | message    | None                                 |
   | project_id | 123456                               |
   | status     | PENDING                              |
   | updated_at | None                                 |
   | version    | 1                                    |
   | zone_id    | 388814ef-3c5d-415e-a866-5b1d13d78dae |
   +------------+--------------------------------------+

List zone exports:

.. code-block:: shell-session

   $ openstack zone export list

Show zone export:

.. code-block:: shell-session

   $ openstack zone export show 6d5acb9d-f3d6-4ed4-96e1-03bc0e405bb5

Show the zone file for the Zone Export:

.. code-block:: shell-session

   $ openstack zone export showfile 6d5acb9d-f3d6-4ed4-96e1-03bc0e405bb5 -f value
   $ORIGIN example.com.
   $TTL 3600

   example.com.  IN NS ns2.exampleprovider.com.
   example.com.  IN NS ns1.exampleprovider.com.
   example.com.  IN SOA ns.exampleprovider.com. admin@example.com 1458678636 7200 300 604800 300

Delete zone export:

.. code-block:: shell-session

   $ openstack zone export delete 6d5acb9d-f3d6-4ed4-96e1-03bc0e405bb5

Working with Zone Imports
-------------------------
Zone imports enable you to import a zone into Designate from a file on the filesystem.

Create a zone import from a file:

.. code-block:: shell-session

   $ openstack zone import create zonefile.txt
   +------------+--------------------------------------+
   | Field      | Value                                |
   +------------+--------------------------------------+
   | created_at | 2016-04-19T20:59:38.000000           |
   | id         | bab6e152-da9f-4dfc-8a59-3f9710fe4894 |
   | message    | None                                 |
   | project_id | 123456                               |
   | status     | PENDING                              |
   | updated_at | None                                 |
   | version    | 1                                    |
   | zone_id    | None                                 |
   +------------+--------------------------------------+

List zone imports:

.. code-block:: shell-session

   $ openstack zone import list

Show zone import:

.. code-block:: shell-session

   $ openstack zone import show 839d8041-1960-4d74-8533-118d52218074

Delete zone import:

.. code-block:: shell-session

   $ openstack zone import delete 839d8041-1960-4d74-8533-118d52218074

Working with Zone Blacklists
----------------------------
Zone blacklist enable you to block any zone pattern from creation.

Create a zone blacklist

.. code-block:: shell-session

   $openstack zone blacklist create --pattern "^example\.com\.$" --description "This is a blacklisted domain."
   +-------------+--------------------------------------+
   | Field       | Value                                |
   +-------------+--------------------------------------+
   | created_at  | 2016-05-10 00:26:07                  |
   | description | This is a blacklisted domain.        |
   | id          | 308ecb82-4952-4476-88b4-9db18fc78e10 |
   | pattern     | ^example.com.$                     |
   | updated_at  | None                                 |
   +-------------+--------------------------------------+

List zone blacklist

.. code-block:: shell-session

   $ openstack zone blacklist list

Show zone blacklist

.. code-block:: shell-session

   $openstack zone blacklist show 308ecb82-4952-4476-88b4-9db18fc78e10

Update zone blacklist

.. code-block:: shell-session

   $openstack zone blacklist set --pattern "^([A-Za-z0-9_\-]+\.)*example\.com\.$" --description "Updated the description" 308ecb82-4952-4476-88b4-9db18fc78e10

Delete a zone blacklist

.. code-block:: shell-session

   $openstack zone blacklist delete 308ecb82-4952-4476-88b4-9db18fc78e10

Working with zone transfer
--------------------------
Zone transfer enable you to perform the transfer of zone ownership to another project.

Create a Zone Transfer Request

.. code-block:: shell-session

   $openstack zone transfer request create --target-project-id 9cc52dd7649c4aa99fa9db2fb94dabb8 53cdcf82-9e32-4a00-a90d-32d6ec5db7e9
   +-------------------+----------------------------------------------------------------------------------------+
   | Field             | Value                                                                                  |
   +-------------------+----------------------------------------------------------------------------------------+
   | created_at        | 2016-05-10 01:39:00                                                                    |
   | description       | None                                                                                   |
   | id                | 98ba1d22-c092-4603-891f-8a0ab04f7e57                                                   |
   | key               | J6JCET2C                                                                               |
   | links             | {u'self':                                                                              |
   |                   | u'http://192.168.11.182:9001/v2/zones/tasks/transfer_requests/98ba1d22-c092-4603-891f- |
   |                   | 8a0ab04f7e57'}                                                                         |
   | project_id        | 10457ad1fe074f4a89bb1e4c0cd83d40                                                       |
   | status            | ACTIVE                                                                                 |
   | target_project_id | 9cc52dd7649c4aa99fa9db2fb94dabb8                                                       |
   | updated_at        | None                                                                                   |
   | zone_id           | 53cdcf82-9e32-4a00-a90d-32d6ec5db7e9                                                   |
   | zone_name         | example.com.                                                                           |
   +-------------------+----------------------------------------------------------------------------------------+

List Zone Transfer Requests

.. code-block:: shell-session

   $openstack zone transfer request list

Show Zone Transfer Request Details

.. code-block:: shell-session

   $openstack zone transfer request show 98ba1d22-c092-4603-891f-8a0ab04f7e57

Update a Zone Transfer Request

.. code-block:: shell-session

   $openstack zone transfer request set 98ba1d22-c092-4603-891f-8a0ab04f7e57 --description "demo transfer"

Delete a Zone Transfer Request

.. code-block:: shell-session

   $openstack zone transfer request delete 98ba1d22-c092-4603-891f-8a0ab04f7e57

Accept a Zone Transfer Request

.. code-block:: shell-session

   $openstack zone transfer accept request  --transfer-id 98ba1d22-c092-4603-891f-8a0ab04f7e57 --key J6JCET2C
   +--------------------------+---------------------------------------------------------------------------------+
   | Field                    | Value                                                                           |
   +--------------------------+---------------------------------------------------------------------------------+
   | created_at               | 2016-05-10 05:02:52                                                             |
   | id                       | a8750f50-d7e6-403a-89d2-e209d62ef60e                                            |
   | key                      | J6JCET2C                                                                        |
   | links                    | {u'self':                                                                       |
   |                          | u'http://192.168.11.182:9001/v2/zones/tasks/transfer_accepts/a8750f50-d7e6      |
   |                          | -403a-89d2-e209d62ef60e', u'zone':                                              |
   |                          | u'http://192.168.11.182:9001/v2/zones/53cdcf82-9e32-4a00-a90d-32d6ec5db7e9'}    |
   | project_id               | 10457ad1fe074f4a89bb1e4c0cd83d40                                                |
   | status                   | COMPLETE                                                                        |
   | updated_at               | 2016-05-10 05:02:52                                                             |
   | zone_id                  | 53cdcf82-9e32-4a00-a90d-32d6ec5db7e9                                            |
   | zone_transfer_request_id | 98ba1d22-c092-4603-891f-8a0ab04f7e57                                            |
   +--------------------------+---------------------------------------------------------------------------------+

Show Zone Transfer Accept

.. code-block:: shell-session

   $openstack zone transfer accept show a8750f50-d7e6-403a-89d2-e209d62ef60e

List Zone Transfer Accept

.. code-block:: shell-session

   $openstack zone transfer accept list

Working with tld
-----------------

tld enable you to manage top level domains.

Create a TLD

.. code-block:: shell-session

   $openstack tld create --name com --description "demo TLD"
   +-------------+--------------------------------------+
   | Field       | Value                                |
   +-------------+--------------------------------------+
   | created_at  | 2016-05-10 05:21:40                  |
   | description | demo TLD                             |
   | id          | a7bba387-712b-4b42-9368-4508642c6113 |
   | name        | com                                  |
   | updated_at  | None                                 |
   +-------------+--------------------------------------+

List TLDs

.. code-block:: shell-session

   $openstack tld list

Show TLD Details

.. code-block:: shell-session

   $openstack tld show a7bba387-712b-4b42-9368-4508642c6113

Update a TLD

.. code-block:: shell-session

   $openstack tld set a7bba387-712b-4b42-9368-4508642c6113 --name org --description "TLD description"

Delete a TLD

.. code-block:: shell-session

   $openstack tld delete a7bba387-712b-4b42-9368-4508642c6113
