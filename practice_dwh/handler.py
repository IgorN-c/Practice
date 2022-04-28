"""High level logic handler."""

import logging

LOGGER = logging.getLogger(__name__)


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
        """Log the name set by the initializer.

        This method plays a role as an entrypoint to the business logic.
        """
        LOGGER.info(self.name)
