"""Entry point for the monitoring service."""

from .logging_setup import configure_logging
from .services.manager import ServiceManager
from .config import load_config


def main() -> None:
    """Start the service."""
    configure_logging()
    config = load_config()
    manager = ServiceManager(config)
    manager.start()


if __name__ == "__main__":
    main()
