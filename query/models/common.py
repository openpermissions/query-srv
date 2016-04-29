# -*- coding: utf-8 -*-
# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

from collections import defaultdict, namedtuple
import json
import logging
import functools

from tornado.gen import coroutine, Return
from tornado.options import options
from tornado import httpclient
from tornado.concurrent import Future
from chub import API
from chub.oauth2 import Read, get_token
from koi import exceptions
from bass.hubkey import parse_hub_key


def reduce_errors(errors):
    """
    raise an error for a list of errors
    :param errors: a list of httpclient.HTTPError
    :return: httpclient.HTTPError
    """
    logging.info('Error: %s', errors)
    http_errors = [e for e in errors if isinstance(e, httpclient.HTTPError)]
    non_http_errors = [e for e in errors if e not in http_errors]
    # if non of the errors are http errors throw a
    # 500 internal error
    if len(non_http_errors) == len(errors):
        logging.error('Non HTTP Errors: %s', errors)
        return exceptions.HTTPError(500, errors[0].args)
    # if there is only one http error, return it
    if len(http_errors) == 1:
        return http_errors[0]
    bad_requests = [err for err in http_errors if err.code == 400]
    # if any error is a bad request, the request is bad
    if bad_requests:
        return bad_requests[0]
    internal_errors = [err for err in http_errors if err.code == 500]
    # if all are internal errors, it must be an internal error
    if len(internal_errors) == len(http_errors):
        return errors[0]
    # TODO we need to build up the scenarios as we go along
    # for now, just raise the first
    return http_errors[0]


def return_exception(func):
    """
    decorator for returning the result
    and exception in a tuple
    :param func: funtion to be wrapped
    :return: a wrapped function
    """
    @coroutine
    @functools.wraps(func)
    def wrapper(*arg, **kw):
        try:
            result = func(*arg, **kw)
            if isinstance(result, Future):
                result = yield result
        except Exception as exc:
            logging.exception('Caught the error and will be processed')
            raise Return((None, exc))
        else:
            raise Return((result, None))
    return wrapper


IndexItem = namedtuple('IndexResult', 'repository,ids')


@coroutine
def get_asset_repositories(source_id_type, source_id):
    """
    Get a list of repository services to query

    :param source_id_type - The id type of the asset to get
    :param source_id - The id of the id type for the asset to get

    :returns: list of IndexItem
    """
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json'}
    api = yield service_client('index', options.url_index)
    endpoint = api.index['entity-types'].asset['id-types'][source_id_type].ids[source_id].repositories
    endpoint.prepare_request(headers=headers,
                             request_timeout=180)
    response = yield endpoint.get()

    raise Return(response)


@coroutine
def get_repositories(ids):
    """
    Get a list of repository services to query

    :param ids: a list of dictionaries containing id & id_type

    :returns: list of IndexItem
    """
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json'}
    api = yield service_client('index', options.url_index)
    endpoint = api.index['entity-types'].asset.repositories
    endpoint.prepare_request(body=json.dumps(ids),
                             headers=headers,
                             request_timeout=180)

    response = yield endpoint.post()

    results = defaultdict(lambda: IndexItem({}, []))

    for item in response.get('data', []):
        for repo in item.pop('repositories', []):
            result = results[repo['repository_id']]

            if not result.repository:
                result.repository.update(repo)

            result.ids.append(item)

    raise Return(results.values())


@coroutine
def get_repository(repository_id):
    """
    Lookup the repository location from the accounts service

    TODO: cache the response

    :param repository_id: the repository's ID
    :returns: a URL
    """
    api = API(options.url_accounts, ca_certs=options.ssl_ca_cert)
    response = yield api.accounts.repositories[repository_id].get()

    raise Return(response)


@coroutine
def repository_request(endpoint, repository, data):
    """
    Make a request to a repository service

    :param endpoint: a chub.API endpoint
    :param repository: a repisotory dict
    :param data: a list of dictionaries containing id & id_type

    :returns: list of results
    """
    if not data:
        raise Return([])

    # Change id & id_type to source_id & source_id_type (temporary
    # until the repo service has been updated)
    data = [{'source_id': i['source_id'], 'source_id_type': i['source_id_type']} for i in data]

    endpoint.prepare_request(
        request_timeout=180,
        headers={'Content-Type': 'application/json',
                 'Accept': 'application/json'},
        body=json.dumps(data))

    rsp_body = yield endpoint.post()

    result = [dict(item.items() + [('repository', repository)])
              for item in rsp_body['data']]
    raise Return(result)


@coroutine
def service_client(service_type, location):
    """
    get an api client for a repository service
    :params service_type: type of the service
    :params location: base url of the repository
    :returns: an api client instance
    """
    token = yield get_token(
        options.url_auth, options.service_id,
        options.client_secret, scope=Read(),
        ca_certs=options.ssl_ca_cert)
    client = API(location, token=token, ca_certs=options.ssl_ca_cert)
    raise Return(client)


def translate_id_pair(source_id):
    """
    Translate an id pair (source_id_type, source_id) into an id that can be processed
    :param source_id: The id
    :return: The translated id
    """
    if source_id['source_id_type'] == 'hub_key':
        parsed = parse_hub_key(source_id['source_id'])
        if parsed['schema_version'] == 's0':
            source_id['source_id_type'] = parsed['id_type']
            source_id['source_id'] = parsed['entity_id']
    return source_id
