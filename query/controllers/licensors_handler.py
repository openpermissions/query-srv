# -*- coding: utf-8 -*-
# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

"""API licensor handler. Queries repository service to get licensor information.
"""
import json

from koi.base import BaseHandler, HTTPError
from tornado import gen, httpclient

from ..models import licensors, common


class LicensorsHandler(BaseHandler):
    """
    Handler for licensors
    """

    @gen.coroutine
    def get(self):
        """
        Retrieve licensors
        """
        source_id_type = self.get_argument('source_id_type', None)
        source_id = self.get_argument('source_id', None)
        if not source_id_type or not source_id:
            raise HTTPError(400, 'Must have "source_id_type" and "source_id" parameters')

        try:
            translated_id = common.translate_id_pair(
                {'source_id_type': source_id_type, 'source_id': source_id})
        except ValueError:
            raise HTTPError(400, '{} is an invalid hub key'.format(source_id))

        try:
            result = yield licensors.get_asset_licensors(
                translated_id['source_id_type'],
                translated_id['source_id']
            )
            self.finish(result)
        except httpclient.HTTPError as exc:
            body = json.loads(exc.response.body)
            raise HTTPError(exc.response.code, body)
