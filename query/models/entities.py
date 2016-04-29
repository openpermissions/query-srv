# -*- coding: utf-8 -*-
# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

from tornado import httpclient
from tornado.gen import coroutine, Return

from . import common


@coroutine
def get_entity(repository_id, entity_type, entity_id):
    """
    Get an entity from a repository

    :param repository_id: the repository that contains the entity
    :param entity_type: a valid entity type (asset, offer or agreement)
    :param entity_id: the entity's ID
    :returns: the entity data from the repository service
    :raises: tornado.httpclient.HTTPError
    """
    endpoint = yield entity_endpoint(repository_id, entity_type)
    if not endpoint:
        raise Return(None)

    try:
        result = yield endpoint[entity_id].get()
    except httpclient.HTTPError as err:
        if err.code == 404:
            raise Return(None)
        else:
            raise

    raise Return(result['data'])


def _pluralise(entity_type):
    # TODO: this may not be needed if we decide to use pluralised entity types
    # in hub keys
    return entity_type + 's'


@coroutine
def entity_endpoint(repository_id, entity_type):
    """
    Return an chub.API endpoint for the repository & entity type

    :param repository_id: the repository that contains the entity
    :param entity_type: a valid entity type (asset, offer or agreement)
    :returns: chub.API instance
    :raises: tornado.httpclient.HTTPError
    """
    try:
        repository = yield common.get_repository(repository_id)
    except httpclient.HTTPError as err:
        if err.code == 404:
            raise Return(None)
        else:
            raise

    url = repository['data']['service']['location']
    api = yield common.service_client('repository', url)
    endpoint = api.repository.repositories[repository_id][_pluralise(entity_type)]

    raise Return(endpoint)
