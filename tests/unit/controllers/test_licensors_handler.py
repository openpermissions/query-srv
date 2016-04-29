# -*- coding: utf-8 -*-
# Copyright 2016 Open Permissions Platform Coalition
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

import os

import pytest
from mock import patch, MagicMock

from koi import define_options
from koi.base import HTTPError
from koi.test_helpers import make_future

from query.controllers.licensors_handler import LicensorsHandler
from query.app import CONF_DIR


future_not_found = make_future(
        {
            'status': 404,
            'errors':
                [
                    {
                        'message': 'Not Found'
                    }
                ]
        }
)

future_asset_repositories = make_future(
    {
        'status': 200,
        'data':
            {
                'repositories':
                    [
                        {
                            'repository_id': 'an_org'
                        }
                    ]
            }
    }
)

future_repository = make_future(
    {
        'status': 200,
        'data': {
            'organisation':
                {
                    'name': 'org name',
                    'organisation_id': 'an_org'
                }
        }
    }
)


def _create_handler():
    handler = LicensorsHandler(MagicMock(), MagicMock())
    handler.finish = MagicMock()
    handler.request.headers = {'Content-Type': 'application/json'}

    def get_arg(arg, default):
        args = {
            'source_id_type': 'a_type',
            'source_id': 'an_id'
        }
        return args.get(arg, default)

    handler.get_argument = get_arg

    return handler


def setup_function(function):
    define_options(os.path.join(CONF_DIR, 'default.conf'))


@patch('query.models.licensors.get_asset_repositories')
@patch('query.models.licensors.get_repository')
def test_get(get_repository, get_asset_repositories):
    source_id_type = 'a_type'
    source_id = 'an_id'
    get_asset_repositories.return_value = future_asset_repositories
    get_repository.return_value = future_repository
    response = {
        'status': 200,
        'data': [
            {
                'name': 'org name',
                'organisation_id': 'an_org'
            }
        ]
    }

    handler = _create_handler()

    # MUT
    handler.get().result()
    handler.finish.assert_called_once_with(response)
    assert handler.get_status() == 200
    get_asset_repositories.assert_called_once_with(source_id_type, source_id)


@patch('query.models.licensors.get_asset_repositories')
def test_get_asset_repositories_not_found(get_asset_repositories):
    source_id_type = 'a_type'
    source_id = 'an_id'
    get_asset_repositories.return_value = future_not_found

    handler = _create_handler()

    # MUT
    with pytest.raises(HTTPError) as excinfo:
        handler.get().result()

    assert excinfo.value.status_code == 404
    assert excinfo.value.errors == [{'message': 'Not Found'}]
    get_asset_repositories.assert_called_once_with(source_id_type, source_id)


@patch('query.models.licensors.get_asset_repositories')
@patch('query.models.licensors.get_repository')
def test_get_repository_not_found(get_repository, get_asset_repositories):
    source_id_type = 'a_type'
    source_id = 'an_id'
    get_asset_repositories.return_value = future_asset_repositories
    get_repository.return_value = future_not_found

    handler = _create_handler()

    # MUT
    with pytest.raises(HTTPError) as excinfo:
        handler.get().result()

    assert excinfo.value.status_code == 404
    assert excinfo.value.errors == [{'message': 'Not Found'}]
    get_asset_repositories.assert_called_once_with(source_id_type, source_id)
    get_repository.assert_called_once_with('an_org')
