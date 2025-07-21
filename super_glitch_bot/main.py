"""Entry point for the monitoring service."""

from .logging_setup import configure_logging
from .services.manager import ServiceManager


def main() -> None:
    """Start the service."""
    logger = configure_logging()
    manager = ServiceManager()
    manager.start()


if __name__ == "__main__":
    main()
