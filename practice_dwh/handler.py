"""High level logic handler."""

import logging

from picnic.database import DatabaseClient

from practice_dwh import PROJECT_ROOT_DIR

LOGGER = logging.getLogger(__name__)
QUERY_PATH = PROJECT_ROOT_DIR / "queries"


class PracticeDwhHandler:
    """Handle practice dwh logic.

    Expose `run()` method as an entrypoint to handle the logic.
    """

    def __init__(self, dwh_client: DatabaseClient):
        """Initialize PracticeDwhHandler class.

        Args:
            dwh_client: Client to connect to Picnic DWH.
        """
        self.dwh_client = dwh_client

    def run(self):
        """Execute ETL to get the total orders (to be) delivered yesterday and today."""
        self._extract()

    def _extract(self):
        orders_yesterday = next(
            self.dwh_client.select(
                query=(QUERY_PATH / "deliveries.sql").read_text()
            ).as_dicts()
        )["delivered_orders"]

        LOGGER.info("Nr. of fulfilled orders yesterday: %s", orders_yesterday)
