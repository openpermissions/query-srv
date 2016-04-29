# -*- coding: utf-8 -*-
# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

from tornado.gen import coroutine, Return
from tornado import httpclient

from . import common


@common.return_exception
@coroutine
def get_asset_offers_from_one_repo(repository, data):
    repository_id = repository['repository_id']
    try:
        repo = yield common.get_repository(repository_id)
    except httpclient.HTTPError as err:
        # Return None if could not get the URL, might be stale index data
        if err.code == 404:
            raise Return(None)
        else:
            raise

    url = repo['data']['service']['location']
    api = yield common.service_client('repository', url)
    endpoint = api.repository.repositories[repository_id].search.offers

    result = yield common.repository_request(endpoint, repository, data)
    raise Return(result)


@common.return_exception
@coroutine
def get_offer_from_one_repo(repository, request, offer_id):
    api = yield common.service_client('repository',
                                      repository['service']['location'])
    endpoint = api.repository.repositories[repository['id']].offers[offer_id]
    headers = request.headers
    try:
        del headers['Authorization']
    except KeyError:
        pass
    endpoint.prepare_request(
        request_timeout=180,
        headers=headers)  # pass on the headers, body can only be None
    rsp_body = yield endpoint.get()
    data = rsp_body['data']
    # only add repository object if data not empty
    if data:
        data['repository'] = repository
    raise Return(data)


@coroutine
def get_asset_offers(ids):
    """
    Get offers from repository services for list of assets

    :param ids: a list of dictionaries containing id & id_type
    """
    repositories = yield common.get_repositories(ids)
    if not repositories:
        raise Return({'status': 200, 'data': []})

    results = yield [get_asset_offers_from_one_repo(repository, data) for repository, data in repositories]

    outputs, errors = zip(*results)
    outputs = [o for o in outputs if o is not None]
    errors = [e for e in errors if e is not None]

    if outputs or not errors:
        raise Return({'status': 200, 'data': sum(outputs, [])})

    raise common.reduce_errors(errors)
