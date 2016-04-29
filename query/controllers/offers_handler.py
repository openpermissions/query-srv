# -*- coding: utf-8 -*-
# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

"""API offers handler. Query repository service to get offers from the db."""
import json

from koi.base import BaseHandler, HTTPError
from tornado import gen, httpclient

from ..models import offers, common


class OffersHandler(BaseHandler):
    """
    Handler for offers
    """
    METHOD_ACCESS = {
        "POST": BaseHandler.READ_ACCESS,
        "OPTIONS": BaseHandler.READ_ACCESS
    }

    @gen.coroutine
    def post(self):
        """
        Retrieve offers by id and id type
        """
        try:
            ids = [common.translate_id_pair(i)
                        for i in self.get_json_body()]
        except ValueError, e:
            raise HTTPError(400, "Invalid id submitted : {}".format(e))

        try:
            result = yield offers.get_asset_offers(ids)
            self.finish(result)
        except httpclient.HTTPError as exc:
            body = json.loads(exc.response.body)
            raise HTTPError(exc.response.code, body)
