"""High level logic handler."""

import logging
from datetime import date
from typing import Dict
from xmlrpc.client import Boolean

from picnic.database import DatabaseClient
from picnic.client.sync import Client

from practice_dwh import PROJECT_ROOT_DIR

LOGGER = logging.getLogger(__name__)
QUERY_PATH = PROJECT_ROOT_DIR / "queries"


class PracticeDwhHandler:
    """Handle practice dwh logic.

    Expose `run()` method as an entrypoint to handle the logic.
    """

    def __init__(
        self,
        dwh_client: DatabaseClient,
        backend_client: Client,
        datalayer_config: dict[str, str],
    ):
        """Initialize PracticeDwhHandler class.

        Args:
            dwh_client: Client to connect to Picnic DWH.
            backend_client: Client to make HTTPS requests to Picnic backends.
        """
        self.dwh_client = dwh_client
        self.backend_client = backend_client
        self.datalayer_config = datalayer_config

    def run(self):
        """Execute ETL to get the total orders (to be) delivered yesterday and today."""
        self._extract_dwh()
        self._extract_datalayer()

    def _extract_dwh(self):
        orders_yesterday = next(
            self.dwh_client.select(
                query=(QUERY_PATH / "deliveries.sql").read_text()
            ).as_dicts()
        )["delivered_orders"]

        LOGGER.info("Nr. of fulfilled orders yesterday: %s", orders_yesterday)

    def _extract_datalayer(self):
        date_today = date.today().strftime("%Y-%m-%d")
        query_params = {
            "deliveryDate": date_today,
            "deliveryDateLast": date_today,
            "includeCancelled": self.datalayer_config["includeCancelled"],
            "excludeTestOrders": self.datalayer_config["excludeTestOrders"],
            }
        response = self.backend_client.get(
            url=f"{self.datalayer_config['url']}/{self.datalayer_config['api_name']}",
            params=query_params,
        )
        response.raise_for_status()

        orders_today = len(response.json()["orders"])
        LOGGER.info("Nr. of fulfilled orders today: %s", orders_today)
