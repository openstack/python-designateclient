============
Installation
============

Install the client from PyPI
----------------------------
The :program:`python-designateclient` package is published on `PyPI`_ and so can be installed using the pip tool, which will manage installing all
python dependencies:

.. code-block:: shell-session

   pip install python-designateclient

*Warning: the packages on PyPI may lag behind the git repo in functionality.*

Setup the client from source
----------------------------
If you want the latest version, straight from github:

.. code-block:: shell-session

    git clone git@github.com:openstack/python-designateclient.git
    cd python-designateclient
    virtualenv .venv
    . .venv/bin/activate
    pip install -r requirements.txt -r test-requirements.txt
    python setup.py install

Setup the client in development mode
------------------------------------

Installing in development mode allows your to make changes to the source code & test directly without having to re-run the "python setup.py install"
step.  You can find out more about `Development Mode`_

.. code-block:: shell-session

    git clone git@github.com:openstack/python-designateclient.git
    cd python-designateclient
    virtualenv .venv
    . .venv/bin/activate
    pip install -r requirements.txt -r test-requirements.txt
    python setup.py develop

.. _Development Mode: https://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode
.. _PyPI: https://pypi.org/project/python-designateclient/
