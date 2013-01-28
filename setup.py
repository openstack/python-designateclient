#!/usr/bin/env python
# Copyright 2012 Managed I.T.
#
# Author: Kiall Mac Innes <kiall@managedit.ie>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import textwrap
from setuptools import setup, find_packages
from monikerclient.openstack.common import setup as common_setup

install_requires = common_setup.parse_requirements(['tools/pip-requires'])
tests_require = common_setup.parse_requirements(['tools/test-requires'])
setup_require = common_setup.parse_requirements(['tools/setup-requires'])
dependency_links = common_setup.parse_dependency_links([
    'tools/pip-requires',
    'tools/test-requires',
    'tools/setup-requires'
])

setup(
    name='python-monikerclient',
    version=common_setup.get_version('python-monikerclient'),
    description='DNS as a Service - Client',
    author='Kiall Mac Innes',
    author_email='kiall@managedit.ie',
    url='https://launchpad.net/python-monikerclient',
    packages=find_packages(exclude=['bin']),
    include_package_data=True,
    test_suite='nose.collector',
    setup_requires=setup_require,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    dependency_links=dependency_links,
    scripts=[
        'bin/moniker',
    ],
    cmdclass=common_setup.get_cmdclass(),
    entry_points=textwrap.dedent("""
        [moniker.cli]
        domain-list = monikerclient.cli.domains:ListDomainsCommand
        domain-get = monikerclient.cli.domains:GetDomainCommand
        domain-create = monikerclient.cli.domains:CreateDomainCommand
        domain-update = monikerclient.cli.domains:UpdateDomainCommand
        domain-delete = monikerclient.cli.domains:DeleteDomainCommand

        record-list = monikerclient.cli.records:ListRecordsCommand
        record-get = monikerclient.cli.records:GetRecordCommand
        record-create = monikerclient.cli.records:CreateRecordCommand
        record-update = monikerclient.cli.records:UpdateRecordCommand
        record-delete = monikerclient.cli.records:DeleteRecordCommand

        server-list = monikerclient.cli.servers:ListServersCommand
        server-get = monikerclient.cli.servers:GetServerCommand
        server-create = monikerclient.cli.servers:CreateServerCommand
        server-update = monikerclient.cli.servers:UpdateServerCommand
        server-delete = monikerclient.cli.servers:DeleteServerCommand
        """),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Internet :: Name Service (DNS)',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Environment :: Console',
        'Environment :: OpenStack',
    ],
)
