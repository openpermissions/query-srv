# -*- coding: utf-8 -*-
# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

import os
import json

import pytest
from mock import patch, Mock, MagicMock

from tornado import httpclient
from koi import define_options
from koi.base import HTTPError
from koi.test_helpers import make_future, gen_test

from query.controllers.offers_handler import OffersHandler
from query.app import CONF_DIR

future_accounts_repositories = make_future([
    {'id': 'repo1', 'service': {'location': 'https://localhost'}}
])


future_repositories = make_future([(
    {'repository_id': 'repo1'},
    [{'source_id': 'https://openpermissions.org/s0/hub1/asset/exampleco/ExampleCoPictureID/1',
     'source_id_type': 'chub'}]
)])
future_repository = make_future(
    {
        'status': 200,
        'data':
            {
                'service':
                    {
                        'location': 'https://localhost',
                        'organisation_id': 'an_org'
                    }
            }
    }
)


def _create_offers_handler():
    handler = OffersHandler(MagicMock(), MagicMock())
    handler.finish = MagicMock()
    handler.request.headers = {'Content-Type': 'application/json'}
    return handler


def setup_function(function):
    define_options(os.path.join(CONF_DIR, 'default.conf'))


@patch('query.models.offers.common.get_repository')
@patch('query.models.offers.common.get_repositories')
@patch('query.models.offers.common.service_client')
def test_post(service_client, get_repositories, get_repository):
    get_repositories.return_value = future_repositories
    get_repository.return_value = future_repository

    response = {'status': 200, 'data': []}
    service_client.return_value = make_future(MagicMock())
    client = yield service_client()
    endpoint = client.repository.repositories[''].search.offers
    endpoint.post.return_value = make_future(response)

    handler = _create_offers_handler()

    # MUT
    handler.request.body = ('[{"source_id":' +
                            '"https://openpermissions.org/s0/hub1/asset/exampleco/ExampleCoPictureID/1",' +
                            '"source_id_type":"chub"}]')

    handler.post().result()
    handler.finish.assert_called_once_with(response)
    assert handler.get_status() == 200
    get_repository.assert_called_once_with('repo1')
    get_repositories.assert_called_once_with(
        [{'source_id': 'https://openpermissions.org/s0/hub1/asset/exampleco/ExampleCoPictureID/1',
          'source_id_type': 'chub'}])


@patch('query.models.offers.common.get_repository')
@patch('query.models.offers.common.get_repositories')
@patch('query.models.offers.common.service_client')
@gen_test
def test_post_with_bad_data(service_client, get_repositories, get_repository):
    get_repositories.return_value = future_repositories
    get_repository.return_value = future_repository

    mock_response = Mock()
    mock_response.body = '{"errors": [{"source_id_type": "", "message": "not supported asset id type"}]}'
    mock_response.code = 400
    exc = httpclient.HTTPError(400, response=mock_response)
    service_client.return_value = make_future(MagicMock())
    client = yield service_client()
    endpoint = client.repository.repositories[''].search.offers
    endpoint.post.side_effect = exc

    handler = _create_offers_handler()

    # MUT
    handler.request.body = ('[{"source_id":' +
                            '"https://openpermissions.org/s0/hub1/asset/exampleco/ExampleCoPictureID/1",' +
                            '"source_id_type":""}]')

    with pytest.raises(HTTPError) as excinfo:
        handler.post().result()

    assert excinfo.value.status_code == mock_response.code
    assert excinfo.value.errors == json.loads(mock_response.body)
