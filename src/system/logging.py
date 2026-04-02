import sys

from loguru import logger


def setup_logging(
    log_level: str, log_file: str, log_in_console: bool = False
) -> None:
    logger.remove()

    logger.add(
        log_file,
        rotation="10 MB",
        retention="7 days",
        level=log_level,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | {level} | "
            "{module}:{function}:{line} | {message}"
        ),
    )
    # Add logs directly to console
    if log_in_console:
        logger.add(
            sys.stderr,
            level=log_level,
            format="{level} | {message}",
        )
