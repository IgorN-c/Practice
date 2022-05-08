"""Entry point of practice_dwh."""

import warnings
from dataclasses import dataclass

from picnic.database import DatabaseClientFactory
from picnic.tools import config_loader, logging
from picnic.tools.general_tools import initiate_logging

from practice_dwh import PROJECT_ROOT_DIR
from practice_dwh.handler import PracticeDwhHandler

LOGGER = logging.getLogger(__name__)
CONFIG_DIR = PROJECT_ROOT_DIR / "config"


@dataclass
class ProjectConfig:
    """Tools that are used by the application.

    This can store instances of external tools to be configured by
    `configure_project()`, e.g DWH, Picnic backends.
    """

    config: dict


def configure_project() -> ProjectConfig:
    """Handle common project configurations.

    Returns:
        Tools that are used by the application.
    """
    # Enable showing the first occurrence of a specific DeprecationWarning
    warnings.simplefilter("once", DeprecationWarning)

    # Configure logging. Logging level is INFO by default
    initiate_logging()

    # Load config
    config = config_loader.load_config(config_dir=CONFIG_DIR)
    LOGGER.debug("Config is successfully loaded.")

    return ProjectConfig(config)


def main():
    """Run project."""
    project_config = configure_project()

    LOGGER.info("'practice-dwh' service initialized.".upper())

    handler = PracticeDwhHandler(
        dwh_client=DatabaseClientFactory.from_config(project_config.config).get_client()
    )
    handler.run()

    LOGGER.info("'practice-dwh' service finished.".upper())


main()
