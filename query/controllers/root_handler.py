# -*- coding: utf-8 -*-
# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

"""API Root handler. Return basic information about the service.
"""

from koi.base import BaseHandler
from tornado.options import options


class RootHandler(BaseHandler):
    """Responsible for providing basic inf. on the service, like:
    + its name
    + current minor version
    """

    METHOD_ACCESS = {
        'GET': BaseHandler.UNAUTHENTICATED_ACCESS
    }

    def initialize(self, **kwargs):
        try:
            self.version = kwargs['version']
        except KeyError:
            raise KeyError('version is required')

    def get(self):
        """Respond with JSON containing service name and current minor version
        of the service.
        """
        msg = {
            'status': 200,
            'data': {
                'service_name': 'Open Permissions Platform Query Service',
                'service_id': options.service_id,
                'version': '{}'.format(self.version)
            }
        }

        self.finish(msg)
