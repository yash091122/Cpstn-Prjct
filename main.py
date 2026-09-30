"""FactForge Orchestration Module Entrypoint."""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("FactForge Orchestration Module initialized.")


if __name__ == "__main__":
    main()
