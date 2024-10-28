from __future__ import annotations

from os import environ
from sys import stderr, stdout

import loguru
from loguru import logger

logger.remove(0)  # remove the pre-configured handler


def isColorSupported():
    if not stdout.isatty():  # vérifie que le terminal est interactif
        return False
    # vérifie que le terminal supporte les couleurs
    term = environ.get("TERM", "")
    return "color" in term or "ansi" in term


def filterStdout(record: loguru.Record) -> bool:
    STDOUT_MAX_LVL = 30
    if record["level"].no > STDOUT_MAX_LVL:
        return False
    return True


def create_filtered_sinks() -> None:
    LVL_FILES = {
        "logs/trace.log": "TRACE",
        "logs/debug.log": "DEBUG",
        "logs/info.log": "INFO",
        "logs/success.log": "SUCCESS",
        "logs/error.log": "ERROR",
        "logs/critical.log": "CRITICAL",
    }
    for file, name in LVL_FILES.items():

        def filter_func(record: loguru.Record, level: str = name):
            return record["level"].name == level

        logger.add(
            sink=file, format=FMT, filter=filter_func, colorize=False, enqueue=True
        )


FMT = "[<lk>{time:DD/MM/YYYY} {time:HH:mm:ss.ms}</lk>] <lvl>{level:8}</lvl> [<cyan>{file}</cyan>:<y>{line}</y>] (<e>{function}</e>) : <lvl>{message}</lvl>"

logger.add(sink="logs/all.log", format=FMT, level="TRACE", colorize=False, enqueue=True)
create_filtered_sinks()  # creates a sink for each log level

logger.add(
    sink=stdout,
    format=FMT,
    level="DEBUG",
    filter=filterStdout,
    colorize=True,
    enqueue=True,
)
logger.add(sink=stderr, format=FMT, level="ERROR", colorize=True, enqueue=True)

_LOGGER: loguru.Logger = logger


def test():
    logger.trace("trace test")
    logger.debug("debug test")
    logger.info("info test")
    logger.success("success test")
    logger.error("error test")
    logger.critical("critical test")
    try:
        1 / 0
    except Exception as e:
        logger.exception("exception test", e)


if __name__ == "__main__":
    test()
