from lib.logger import _LOGGER
from models.bot import Tavernier


async def on_ready(tavernier: Tavernier) -> None:
    _LOGGER.debug(f"{tavernier.user.name} opened the Tavern.")  # 26/05/2024 13:39:47
    _LOGGER.info("---------------------------------")
    _LOGGER.info("Displaying current log levels :")
    _LOGGER.critical("CRITICAL")
    _LOGGER.error("ERROR")
    _LOGGER.warning("WARNING")
    _LOGGER.info("INFO")
    _LOGGER.debug("DEBUG")
    _LOGGER.trace("TRACE")
    _LOGGER.info("---------------------------------")
