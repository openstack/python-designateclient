======================
python-designateclient
======================

python-designateclient provides python bindings and command line tools for both
Designate v1 and v2 APIs.

The :doc:`Python API bindings <bindings>` are provided by the
:program:`designateclient` module.

There are two separate command line interfaces to work with the two API
versions:

v2: the designate plugin for the :program:`openstack` command line tool.  More information can be
found on the :doc:`designate v2 command line tool page <shell-v2>`.

v1: the :program:`designate` command line tool.  More information can be found
on the :doc:`designate v1 command line tool page <shell>`.

You'll need credentials for an OpenStack cloud that implements the Designate
API in order to use the client.

Contents
======================

.. toctree::
   :maxdepth: 1

   installation
   bindings
   shell-v2
   shell-v2-examples
   shell
   shell-examples
   contributing
   functional-tests

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Cloud DNS: http://www.hpcloud.com/products-services/dns
