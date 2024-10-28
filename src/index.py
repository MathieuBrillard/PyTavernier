import asyncio
from logging import Handler, LogRecord
from pathlib import Path
from tomllib import TOMLDecodeError, load

from lib.logger import _LOGGER
from models.bot import Tavernier

try:
    config_file = Path("config", "config.toml")
    with open(config_file, "rb") as f:
        config = load(f)
        PREFIX = config["DISCORD"]["prefix"]
        CLIENT_ID = config["DISCORD"]["client_id"]
        TOKEN = config["DISCORD"]["token"]
except FileNotFoundError:
    _LOGGER.critical("The toml config file was not found.")
except TOMLDecodeError:
    _LOGGER.critical("The toml config file is malformed.")
except KeyError as e:
    _LOGGER.critical(f"A required key in config file was not found: {e}")


class LoguruHandler(Handler):
    def __init__(self, level=0):
        Handler.__init__(self, level)

    def emit(self, record: LogRecord):
        # This will forward records from the `logging` module to `loguru`
        loguru_level = record.levelname
        logger_opt = _LOGGER.opt(exception=record.exc_info)
        if loguru_level == "DEBUG":
            loguru_level = "TRACE"
        logger_opt.log(loguru_level, record.getMessage())

    def setFormatter(self, *any):
        return


@_LOGGER.catch
def main():
    intents = Tavernier.get_needed_intents()
    tavernier = Tavernier(
        PREFIX,
        description="description test",
        application_id=CLIENT_ID,
        intents=intents,
    )
    asyncio.run(tavernier.up_and_running())
    tavernier.run(token=TOKEN, log_handler=LoguruHandler(), log_level=1)


if __name__ == "__main__":
    main()
