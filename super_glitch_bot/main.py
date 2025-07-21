"""Entry point for the monitoring service."""

import asyncio

from .logging_setup import configure_logging
from .services.manager import ServiceManager
from .config import load_config


async def main() -> None:
    """Start the service."""
    configure_logging()
    config = load_config()
    manager = ServiceManager(config)
    try:
        await manager.start()
    except KeyboardInterrupt:
        pass
    finally:
        await manager.stop_monitoring()


if __name__ == "__main__":
    asyncio.run(main())
