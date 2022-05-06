"""High level logic handler."""

from asyncio.log import logger
import logging

from picnic.database import DatabaseClientFactory
from picnic.definitions import Environment

from practice_dwh import PROJECT_ROOT_DIR

LOGGER = logging.getLogger(__name__)
QUERY_PATH = PROJECT_ROOT_DIR / "queries"


class PracticeDwhHandler:
    """Handle practice dwh logic.

    Expose `run()` method as an entrypoint to handle the logic.
    """

    def __init__(self, name: str):
        """Initialize PracticeDwhHandler class.

        Args:
            name: Name to process.
        """
        self.name = name

    def run(self):
        """Execute ETL to get the total orders (to be) delivered yesterday and today.
        """
        self._extract()

    def _extract(self):
        dwh_client = DatabaseClientFactory(
            Environment("local"),
            database="picnic_nl_prod", 
            warehouse="ANALYSIS",
            role="analyst",
            account="uj82639.eu-west-1",
            username="igor.neifach@teampicnic.com",
        ).get_client()
        orders_yesterday = next(
            dwh_client.select(query=(QUERY_PATH/"deliveries.sql").read_text()).as_dicts()
        )["delivered_orders"]

        LOGGER.info(f"Nr. of fulfilled orders yesterday: {orders_yesterday}")
