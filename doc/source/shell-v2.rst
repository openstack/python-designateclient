=============================
designate v2 cli and examples
=============================

In order to use the v2 you need *python-openstackclient* available.

::

    $ pip install python-openstackclient


Using the client
----------------

Source credentials first

::

    $ source ~/openrc

Or you can use the ~/.config/openstack/clouds.yaml approach.

.. note::

    This required you to pass in --os-cloud <cloudname> after the "openstack" part.

We can now try to create a primary zone

.. code-block:: shell-session

    $ openstack zone create example.net. --email foo@example.org

Create a A type recordset with some records in it.

.. code-block:: shell-session

    $ openstack recordset create example.net --type A www --records 10.0.0.1 10.0.0.2

Set a PTR record for a Floating IP

.. code-block:: shell-session

    $ openstack ptr record set RegionOne:5c02c519-4928-4a38-bd10-c748c200912f mail.example.net.
