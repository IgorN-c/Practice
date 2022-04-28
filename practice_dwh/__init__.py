"""Project root."""

from pathlib import Path

from picnic.monitoring import Monitoring

PROJECT_ROOT_DIR = Path(__file__).parent.resolve()

monitoring = Monitoring()
monitoring.configure_sentry(project_name=PROJECT_ROOT_DIR.parent.name)
monitoring.start()
