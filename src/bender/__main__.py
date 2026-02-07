"""Entry point for the Bender application."""

import asyncio
import logging

from bender.app import create_app, start
from bender.config import load_settings

logger = logging.getLogger(__name__)


async def main() -> None:
    """Start the Bender application."""
    settings = load_settings()
    logger.info(
        "Bender starting (workspace=%s, port=%d)",
        settings.bender_workspace,
        settings.bender_api_port,
    )

    app = create_app(settings)
    await start(app, settings)


if __name__ == "__main__":
    asyncio.run(main())
