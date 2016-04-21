====================================
Openstack Command Line Tool Examples
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
