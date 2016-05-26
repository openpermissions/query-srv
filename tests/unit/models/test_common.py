# -*- coding: utf-8 -*-
# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

import json
from functools import partial

import pytest

from koi.test_helpers import make_future, gen_test
from mock import patch, Mock, MagicMock
from tornado.concurrent import Future
from tornado.ioloop import IOLoop

from query.models.common import (return_exception, get_repositories,
                                 repository_request, IndexItem, translate_id_pair)


options_patch = patch('query.models.common.options')


def setup_function(function):
    options_patch.start()


def teardown_function(function):
    options_patch.stop()


def test_return_exception_no_exception():

    @return_exception
    def no_errors():
        return 'foo'

    result = no_errors().result()
    assert result == ('foo', None)


def test_return_exception_future_no_exception():

    @return_exception
    def future_no_errors():
        f = Future()
        f.set_result('foo')
        return f

    result = future_no_errors().result()
    assert result == ('foo', None)


def test_return_exception_with_exception():

    exc = ValueError('foo')

    @return_exception
    def raise_exception():
        raise exc

    result = raise_exception().result()
    assert result == (None, exc)


@patch('query.models.common.service_client')
@gen_test
def test_get_repositories(service_client):
    """Test successfully getting a list of repository IDs from the index"""
    response = [
        {'id': 'an asset', 'id_type': 'an_id_type',
         'repositories': [{'repository_id': 'a'}, {'repository_id': 'b'}]},
        {'id': 'another asset', 'id_type': 'an_id_type',
         'repositories': [{'repository_id': 'b'}, {'repository_id': 'c'}]},
    ]
    service_client.return_value = make_future(MagicMock())
    client = yield service_client()
    endpoint = client.index['entity-types'].asset.repositories
    endpoint.post.return_value = make_future({'data': response})

    ids = [
        {'id': 'an asset', 'id_type': 'an_id_type'},
        {'id': 'another asset', 'id_type': 'an_id_type'}
    ]

    result = yield get_repositories(ids)

    # check mock
    assert endpoint.post.call_count == 1
    endpoint.prepare_request.assert_called_once_with(
        body=json.dumps(ids),
        request_timeout=180,
        headers={'Accept': 'application/json',
                 'Content-Type': 'application/json'})

    # check result
    assert sorted(result) == [
        IndexItem({'repository_id': 'a'},
                  [{'id': 'an asset', 'id_type': 'an_id_type'}]),
        IndexItem({'repository_id': 'b'},
                  [{'id': 'an asset', 'id_type': 'an_id_type'},
                   {'id': 'another asset', 'id_type': 'an_id_type'}]),
        IndexItem({'repository_id': 'c'},
                  [{'id': 'another asset', 'id_type': 'an_id_type'}]),
    ]


@patch('query.models.common.service_client')
@gen_test
def test_get_repositories_empty_result(service_client):
    """Test receiving an empty list from the index"""
    service_client.return_value = make_future(MagicMock())
    client = yield service_client()
    endpoint = client.index['entity-types'].asset.repositories
    endpoint.post.return_value = make_future({})

    ids = [
        {'id': 'an asset', 'id_type': 'an_id_type'},
        {'id': 'another asset', 'id_type': 'an_id_type'},
    ]

    result = yield get_repositories(ids)

    assert result == []


@gen_test
def test_repository_request():
    """Test data sent to repository service"""
    repository = Mock()
    endpoint = Mock()
    endpoint.post.return_value = make_future({'data': [
        {'a': 'something'},
        {'b': 'other thing'},
    ]})
    data = [
        {'source_id': 1, 'source_id_type': 'a'},
        {'source_id': 2, 'source_id_type': 'b'},
    ]

    result = yield repository_request(endpoint, repository, data)

    assert result == [
        {'a': 'something', 'repository': repository},
        {'b': 'other thing', 'repository': repository},
    ]
    # check request body was compatible with repo service
    assert endpoint.prepare_request.call_args[1]['body'] == json.dumps([
        {'source_id': 1, 'source_id_type': 'a'},
        {'source_id': 2, 'source_id_type': 'b'},
    ])


def test_repository_request_with_empty_data():
    repository = Mock()
    endpoint = Mock()

    result = IOLoop.current().run_sync(partial(repository_request, endpoint,
                                               repository, []))

    assert result == []
    assert not endpoint.post.called


def test_repository_request_with_empty_response():
    repository = Mock()
    endpoint = Mock()
    endpoint.post.return_value = make_future({'data': []})

    result = IOLoop.current().run_sync(partial(repository_request, endpoint,
                                               repository, []))

    assert result == []


def test_translate_id_pair():
    original_id = {'source_id_type': 'A_tYpE', 'source_id': 'an_id'}
    translated_id = translate_id_pair(original_id)
    assert translated_id == {'source_id_type': 'a_type', 'source_id': 'an_id'}


def test_translate_id_pair_hub_key_s1():
    original_id = {
        'source_id_type': 'hub_key',
        'source_id': 'https://openpermissions.org/s1/hub1/0123456789abcdef0123456789abcdef/asset/abcdef0123456789abcdef0123456789'
    }
    translated_id = translate_id_pair(original_id)
    assert translated_id == original_id


def test_translate_id_pair_hub_key_s1_corrupt():
    original_id = {
        'source_id_type': 'hub_key',
        'source_id': 'https://openpermissions.org/s1/hub1/0123456789abcdef0123456789abcdef/asset/abcdef0123456789abcdefxyz'
    }
    with pytest.raises(ValueError) as exc:
        translate_id_pair(original_id)
    assert exc


def test_translate_id_pair_hub_key_s0():
    original_id = {
        'source_id_type': 'hub_key',
        'source_id': 'https://openpermissions.org/s0/hub1/asset/maryevans/maryevanspictureid/10413373'
    }
    translated_id = translate_id_pair(original_id)
    assert translated_id == {'source_id_type': 'maryevanspictureid', 'source_id': '10413373'}
