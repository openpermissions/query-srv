# -*- coding: utf-8 -*-
# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

from tornado.gen import coroutine, Return

from koi.base import HTTPError

from .common import (get_asset_repositories,
                     get_repository, return_exception)


@return_exception
@coroutine
def get_licensors_from_one_repo(repository):
    result = yield get_repository(repository['repository_id'])

    raise Return(result)


@coroutine
def get_asset_licensors(source_id_type, source_id):
    """
    Get licensors from repository services for list of assets

    :param source_id_type - The id type of the asset to get
    :param source_id - The id of the id type for the asset to get
    """
    response = yield get_asset_repositories(source_id_type, source_id)
    if 'errors' in response:
        raise HTTPError(response['status'], response['errors'])

    outputs = []
    for repository in response['data']['repositories']:
        result = (yield get_licensors_from_one_repo(repository))[0]
        if 'errors' in result:
            raise HTTPError(result['status'], result['errors'])
        if 'data' in result:
            outputs.append(result['data']['organisation'])
    raise Return({'status': 200, 'data': outputs})
