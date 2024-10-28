import importlib

from discord import Intents
from discord.ext import commands

from commands import __all__ as tavernier_commands
from lib.logger import _LOGGER
from models.music.queue_manager import QueueManager


class Tavernier(commands.Bot):
    def __init__(self, prefix: str, **kwargs) -> None:
        super().__init__(prefix, max_messages=30, **kwargs)
        self._music_queue_manager = QueueManager()

    @staticmethod
    def get_needed_intents() -> Intents:
        _LOGGER.info("Getting discord intents...")
        intents = Intents.default()
        intents.guilds = True
        intents.messages = True
        intents.message_content = True
        intents.emojis_and_stickers = True
        return intents

    @_LOGGER.catch
    async def up_and_running(self) -> None:
        _LOGGER.opt(colors=True).info(
            "\n<m>"
            + " _____                          _           ____        \n"
            + "|_   _|_ ___   _____ _ __ _ __ (_) ___ _ __|  _ \\ _   _ \n"
            + "  | |/ _` \\ \\ / / _ \\ '__| '_ \\| |/ _ \\ '__| |_) | | | |\n"
            + "  | | (_| |\\ V /  __/ |  | | | | |  __/ |  |  __/| |_| |\n"
            + "  |_|\\__,_| \\_/ \\___|_|  |_| |_|_|\\___|_|  |_|    \\__, |\n"
            + "                                                  |___/</m>\n\n"
        )
        await self.load_events()
        await self.load_commands()

    async def load_commands(self) -> None:
        _LOGGER.info("Loading commands...")
        success = True
        for cmd_name in tavernier_commands:
            try:
                cmd = importlib.import_module(f"commands.{cmd_name}")
                cog_class = getattr(  # get the actual cmd class
                    cmd, cmd_name.capitalize()
                )
                await self.add_cog(cog_class(self), guild=True)
            except Exception as e:
                _LOGGER.exception(f"Error while loading command: '{cmd_name}':", e)
                success = False
        if success is True:
            _LOGGER.success("All commands loaded successfully !")

    async def load_events(self) -> None:
        _LOGGER.info("Loading events...")
        # @tavernier.event

    @property
    def get_music_manager(self):
        return self._music_queue_manager
