"""High level logic handler."""

import logging
from datetime import date

from picnic.client.sync import Client
from picnic.database import DatabaseClient

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
            datalayer_config: Configuration for datalayer domain access.
        """
        self.dwh_client = dwh_client
        self.backend_client = backend_client
        self.datalayer_config = datalayer_config
        self.orders_yesterday = 0
        self.orders_today = 0
        self.orders_since_yesterday = 0

    def run(self):
        """Execute ETL to get the total orders (to be) delivered yesterday and today."""
        self._extract_dwh()
        self._extract_datalayer()
        self._transform()
        self._load()

    def _extract_dwh(self):
        self.orders_yesterday = next(
            self.dwh_client.select(
                query=(QUERY_PATH / "deliveries.sql").read_text()
            ).as_dicts()
        )["delivered_orders"]

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

        self.orders_today = len(response.json()["orders"])

    def _transform(self):
        self.orders_since_yesterday = self.orders_yesterday + self.orders_today

    def _load(self):
        LOGGER.info(
            """\n
            ===========================================
            Nr. of fulfilled orders yesterday: %s\n
            Nr. of fulfilled orders today: %s\n
            ----------------
            TOTAL: %s\n
            ===========================================
            """,
            self.orders_yesterday,
            self.orders_today,
            self.orders_since_yesterday,
        )
