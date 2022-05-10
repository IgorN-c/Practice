"""Test practice_dwh.handler module."""

# pylint: disable=protected-access

from unittest.mock import MagicMock, Mock

import pytest
from requests import HTTPError

from practice_dwh.handler import PracticeDwhHandler


def test__extract_dwh_successful(project_config):
    """Successful test extract yesterday's delivered orders."""

    # define DWH mock client and stub response
    dwh_select_response = MagicMock()
    dwh_select_response.as_dicts.return_value = iter([{"delivered_orders": 9}])
    dwh_client = Mock()
    dwh_client.select.return_value = dwh_select_response

    # define a mock Picnic Backend client
    backend_client = Mock()

    handler = PracticeDwhHandler(
        dwh_client=dwh_client,
        backend_client=backend_client,
        datalayer_config=project_config.config["datalayer"],
    )
    handler._extract_dwh()

    assert handler.orders_yesterday == 9


def test__extract_datalayer_successful(project_config):
    """Successful test extract today's delivered orders."""

    # define DWH mock client
    dwh_client = Mock()

    # define a mock Picnic Backend client and stub response
    datalayer_response = Mock()
    datalayer_response.json.return_value = {
        "orders": [{"order_id": 1}, {"order_id": 2}]
    }
    backend_client = Mock()
    backend_client.get.return_value = datalayer_response

    handler = PracticeDwhHandler(
        dwh_client=dwh_client,
        backend_client=backend_client,
        datalayer_config=project_config.config["datalayer"],
    )
    handler._extract_datalayer()

    assert handler.orders_today == 2


def test__extract_datalayer_bad_request(project_config):
    """HTTPError is raised when `response.raise_for_status` raises HTTPError."""

    # define DWH mock client and stub response
    dwh_client = Mock()

    # define Picnic Backend session mock client and stub response
    datalayer_response = Mock()
    datalayer_response.raise_for_status.side_effect = HTTPError()
    backend_client = Mock()
    backend_client.get.return_value = datalayer_response

    handler = PracticeDwhHandler(
        dwh_client=dwh_client,
        backend_client=backend_client,
        datalayer_config=project_config.config["datalayer"],
    )

    with pytest.raises(HTTPError):
        handler._extract_datalayer()
