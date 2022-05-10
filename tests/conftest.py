"""Shared conftest among all tests."""

from unittest.mock import Mock

import pytest


@pytest.fixture()
def project_config() -> Mock:
    """Fixture with project configuration."""
    return Mock(
        config={
            "datalayer": {
                "url": "https://datalayer-address-dev.nl.picnicinternational.com",
                "api_name": "api/number/order",
                "includeCancelled": False,
                "excludeTestOrders": False,
            },
        }
    )
