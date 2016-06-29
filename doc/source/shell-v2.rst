=========================================================
OpenStack Command Line Tool (compatible with v2 API only)
=========================================================

The python-designateclient package comes with a plugin for the openstack
command line tool (installed as :program:`openstack`).  This can be used to
access a Designate API without having to manipulate JSON by hand, it can also
produce the output in a variety of formats (JSON, CSV) and allow you to select
columns to be displayed.

Installation
------------

Both *python-openstackclient* and *python-designateclient* must be installed:

::

    $ pip install python-openstackclient python-designateclient


Configuration
-------------

:program:`openstack` requires certain information to talk to the REST API.  An
in-depth explanation is covered in the
`OpenStack Client configuration documentation`_.

Using the Command Line Tool
---------------------------

With enough details now in the environment, you can use the
:program:`openstack` to create a zone and populate it with some records:

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

Now that the zone has been created, we can start adding records.

You'll note that the zone name (example.com) has a trailing ``.``, as per
the DNS standard, and we didn't set a TTL.

.. code-block:: shell-session

  $ openstack recordset create --type A --records 192.0.2.20 example.com. www
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

Designate-specific Subcommands
------------------------------

Aside from the ``zone create`` and ``recordset create`` subcommands, this is
the full list of subcommands that enable Designate V2 support:

============================  ====================================================== ===============
subcommand                    Notes                                                  Admin Required
============================  ====================================================== ===============
zone create                   Create new zone
zone list                     List zones
zone show                     Show zone details
zone set                      Set zone properties
zone delete                   Delete zone
recordset create              Create new recordset
recordset list                List recordsets
recordset list all            List all recordsets in all zones
recordset show                Show recordset details
recordset set                 Set recordset properties
recordset delete              Delete recordset
ptr record list               List floatingip ptr records
ptr record show               Show floatingip ptr record details
ptr record set                Set floatingip ptr record
ptr record unset              Unset floatingip ptr record
zone export create            Export a Zone
zone export list              List Zone Exports
zone export show              Show a Zone Export
zone export delete            Delete a Zone Export
zone export showfile          Show the zone file for the Zone Export
zone import create            Import a Zone from a file on the filesystem
zone import list              List Zone Imports
zone import show              Show a Zone Import
zone import delete            Delete a Zone Import
zone transfer request create  Create new zone transfer request
zone transfer request list    List Zone Transfer Requests
zone transfer request show    Show Zone Transfer Request Details
zone transfer request set     Set a Zone Transfer Request
zone transfer request delete  Delete a Zone Transfer Request
zone transfer accept request  Accept a Zone Transfer Request
zone transfer accept list     List Zone Transfer Accepts
zone transfer accept show     Show Zone Transfer Accept
zone abandon                  Abandon a zone
zone axfr                     AXFR a zone
zone blacklist create         Create new blacklist                                   Yes
zone blacklist list           List blacklists                                        Yes
zone blacklist show           Show blacklist details                                 Yes
zone blacklist set            Set blacklist properties                               Yes
zone blacklist delete         Delete blacklist                                       Yes
tld create                    Create new tld                                         Yes
tld list                      List tlds                                              Yes
tld show                      Show tld details                                       Yes
tld set                       Set tld properties                                     Yes
tld delete                    Delete tld                                             Yes
============================  ====================================================== ===============

Built-in Designate Documentation
--------------------------------

You'll find complete documentation on the shell by running:
``openstack --help``

For a specific command, you can execute: ``openstack subcommand help``

.. _OpenStack Client configuration documentation: http://docs.openstack.org/developer/python-openstackclient/configuration.html
