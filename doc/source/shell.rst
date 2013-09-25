===========================
designate command line tool
===========================

The python-designateclient package comes with a command line tool (installed as :program:`designate`), this can be used to access a Designate API
without having to manipulate JSON by hand, it can also produce the output in a variety of formats (JSON, CSV) and allow you to select columns to be
displayed.

Credentials
-----------

As with any OpenStack utility, :program:`designate` requires certain information to
talk to the REST API, username, password, auth url (from where the other required
endpoints are retrieved once you are authenticated).

To provide your access credentials (username, password, tenant name or tenant id)
you can pass them on the command line with the ``--os-username``, ``--os-password``,  ``--os-tenant-name`` or ``--os-tenant-id``
params, but it's easier to just set them as environment variables::

    export OS_USERNAME=openstack
    export OS_PASSWORD=yadayada
    export OS_TENANT_NAME=myproject
    export OS_TENANT_ID=123456789

You will also need to define the authentication url with ``--os-auth-url``
or set is as an environment variable as well::

    export OS_AUTH_URL=https://example.com:5000/v2.0/

Since Keystone can return multiple regions in the Service Catalog, you
can specify the one you want with ``--os-region-name`` (or
``export OS_REGION_NAME``). It defaults to the first in the list returned.

Using the command line tool
---------------------------

With enough details now in environment, you can use the designate client to create a domain & populate it with some records:

.. code-block:: shell-session

   $ designate domain-create --name doctestdomain.eu. --email admin@doctestdomain.eu
   +-------------+--------------------------------------+
   | Field       | Value                                |
   +-------------+--------------------------------------+
   | description | None                                 |
   | created_at  | 2013-09-19T11:45:25.295355           |
   | updated_at  | None                                 |
   | email       | admin@doctestdomain.eu               |
   | ttl         | 3600                                 |
   | serial      | 1379591125                           |
   | id          | eacbe2a5-95f1-4a9f-89f5-b9c58009b163 |
   | name        | doctestdomain.eu.                    |
   +-------------+--------------------------------------+

You can see more details on the arguments domain-create accepts at the `REST API create-domain`_.

Now that the domain has been created, we can start adding records.

You'll note that the name (www.doctestdomain.eu) has a trailing ``.``, as per the DNS standard, we didn't set a TTL and we had to specify the parent
zone/domain by domain_id ``eacbe2a5-95f1-4a9f-89f5-b9c58009b163``.

.. code-block:: shell-session

  $  designate record-create eacbe2a5-95f1-4a9f-89f5-b9c58009b163 --name www.doctestdomain.eu. --type A --data 1.2.3.4
  +-------------+--------------------------------------+
  | Field       | Value                                |
  +-------------+--------------------------------------+
  | name        | www.doctestdomain.eu.                |
  | data        | 1.2.3.4                              |
  | created_at  | 2013-09-19T13:44:42.295428           |
  | updated_at  | None                                 |
  | id          | 147f6082-8466-4951-8d13-37a10e92b11e |
  | priority    | None                                 |
  | ttl         | None                                 |
  | type        | A                                    |
  | domain_id   | eacbe2a5-95f1-4a9f-89f5-b9c58009b163 |
  | description | None                                 |
  +-------------+--------------------------------------+

subcommands
-----------

We've already seen the ``domain-create`` and ``record-create`` subcommands, here the full list of subcommands:

======================= ====================================================== ===============
subcommand              Notes                                                  Admin Required
======================= ====================================================== ===============
diagnostics-ping        Ping a service on a given host
diagnostics-sync-all    Sync Everything
diagnostics-sync-domain Sync a single Domain
diagnostics-sync-record Sync a single Record
domain-create           Create Domain
domain-delete           Delete Domain
domain-get              Get Domain
domain-list             List Domains
domain-servers-list     List Domain Servers
domain-update           Update Domain
help                    print detailed help for another command
record-create           Create Record
record-delete           Delete Record
record-get              Get Record
record-list             List Records
record-update           Update Record
report-count-all        Get count totals for all tenants, domains and records
report-count-domains    Get counts for total domains
report-count-records    Get counts for total records
report-count-tenants    Get counts for total tenants
report-tenant-domains   Get a list of domains for given tenant
report-tenants-all      Get list of tenants and domain count for each
server-create           Create Server
server-delete           Delete Server
server-get              Get Server
server-list             List Servers
server-update           Update Server
======================= ====================================================== ===============

Builtin designate documentation
-------------------------------

You'll find complete documentation on the shell by running
``designate --help``::

    usage: designate [--version] [-v] [--log-file LOG_FILE] [-q] [-h] [--debug]
                     [--os-endpoint OS_ENDPOINT] [--os-auth-url OS_AUTH_URL]
                     [--os-username OS_USERNAME] [--os-password OS_PASSWORD]
                     [--os-tenant-id OS_TENANT_ID]
                     [--os-tenant-name OS_TENANT_NAME] [--os-token OS_TOKEN]
                     [--os-service-type OS_SERVICE_TYPE]
                     [--os-region-name OS_REGION_NAME]
                     [--sudo-tenant-id SUDO_TENANT_ID] [--insecure]

    Designate Client

    optional arguments:
      --version             show program's version number and exit
      -v, --verbose         Increase verbosity of output. Can be repeated.
      --log-file LOG_FILE   Specify a file to log output. Disabled by default.
      -q, --quiet           suppress output except warnings and errors
      -h, --help            show this help message and exit
      --debug               show tracebacks on errors
      --os-endpoint OS_ENDPOINT
                            Defaults to env[OS_DNS_ENDPOINT]
      --os-auth-url OS_AUTH_URL
                            Defaults to env[OS_AUTH_URL]
      --os-username OS_USERNAME
                            Defaults to env[OS_USERNAME]
      --os-password OS_PASSWORD
                            Defaults to env[OS_PASSWORD]
      --os-tenant-id OS_TENANT_ID
                            Defaults to env[OS_TENANT_ID]
      --os-tenant-name OS_TENANT_NAME
                            Defaults to env[OS_TENANT_NAME]
      --os-token OS_TOKEN   Defaults to env[OS_SERVICE_TOKEN]
      --os-service-type OS_SERVICE_TYPE
                            Defaults to env[OS_DNS_SERVICE_TYPE], or 'dns'
      --os-region-name OS_REGION_NAME
                            Defaults to env[OS_REGION_NAME]
      --sudo-tenant-id SUDO_TENANT_ID
                            Defaults to env[DESIGNATE_SUDO_TENANT_ID]
      --insecure            Explicitly allow 'insecure' SSL requests

    Commands:
      diagnostics-ping  Ping a service on a given host
      diagnostics-sync-all  Sync Everything
      diagnostics-sync-domain  Sync a single Domain
      diagnostics-sync-record  Sync a single Record
      domain-create  Create Domain
      domain-delete  Delete Domain
      domain-get     Get Domain
      domain-list    List Domains
      domain-servers-list  List Domain Servers
      domain-update  Update Domain
      help           print detailed help for another command
      record-create  Create Record
      record-delete  Delete Record
      record-get     Get Record
      record-list    List Records
      record-update  Update Record
      report-count-all  Get count totals for all tenants, domains and records
      report-count-domains  Get counts for total domains
      report-count-records  Get counts for total records
      report-count-tenants  Get counts for total tenants
      report-tenant-domains  Get a list of domains for given tenant
      report-tenants-all  Get list of tenants and domain count for each
      server-create  Create Server
      server-delete  Delete Server
      server-get     Get Server
      server-list    List Servers
      server-update  Update Server

.. _REST API create-domain: https://designate.readthedocs.org/en/latest/rest/domains.html#create-domain
