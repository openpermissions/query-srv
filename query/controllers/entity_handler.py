# -*- coding: utf-8 -*-
# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

from bass.hubkey import parse_hub_key
from koi.base import BaseHandler, HTTPError
from tornado.gen import coroutine
from tornado.web import MissingArgumentError
from tornado import  httpclient
from ..models.entities import get_entity


class EntityHandler(BaseHandler):
    """
    Handler for querying entities using their hub key

    NOTE: s0 hub keys are unsupported because the do not contain the repository
    ID
    """
    @coroutine
    def get(self, repository_id=None, entity_type=None, entity_id=None):
        if repository_id is None:
            try:
                hub_key = self.get_query_argument('hub_key')
            except MissingArgumentError:
                raise HTTPError(400, 'hub_key parameter is required')

            try:
                parts = parse_hub_key(hub_key)
            except ValueError:
                raise HTTPError(404, 'Invalid hub key')

            if parts['schema_version'] == 's0':
                raise HTTPError(404, 'Only hub keys matching '
                                'schema >= s1 are supported')
        else:
            parts = {
                'repository_id': repository_id,
                'entity_type': entity_type,
                'entity_id': entity_id
            }

        try:
            entity = yield get_entity(parts['repository_id'],
                                      parts['entity_type'],
                                      parts['entity_id'])
        except httpclient.HTTPError, e:
            raise HTTPError(e.code, e.message)

        if not entity:
            raise HTTPError(404, 'Not found')

        self.finish({'status': 200, 'data': entity})
