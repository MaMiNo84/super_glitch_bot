"""Entry point for running the monitoring service."""

import asyncio

from super_glitch_bot.main import main

if __name__ == "__main__":
    asyncio.run(main())
