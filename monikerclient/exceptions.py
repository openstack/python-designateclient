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


class Base(Exception):
    pass


class ResourceNotFound(Base):
    pass


class RemoteError(Base):
    def __init__(self, message=None, code=None, type=None, errors=None,
                 request_id=None):
        super(RemoteError, self).__init__(message)

        self.message = message
        self.code = code
        self.type = type
        self.errors = errors
        self.request_id = request_id


class Unknown(RemoteError):
    pass


class BadRequest(RemoteError):
    pass


class Forbidden(RemoteError):
    pass


class Conflict(RemoteError):
    pass


class NotFound(RemoteError):
    pass
