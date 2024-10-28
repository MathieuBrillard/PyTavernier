from discord import VoiceClient
from discord.ext import commands

from lib.logger import _LOGGER
from models.music.queue import Queue


class QueueManager:
    def __init__(self):
        self._queues = {}

    async def cleanup(self, vc: VoiceClient, guild_id: int):
        _LOGGER.info("Client is cleaning up voice connection...")
        try:
            if vc is not None:
                await vc.disconnect(force=True)
            if guild_id in self._queues.keys():
                self._queues.pop(guild_id)
        except Exception as e:
            _LOGGER.exception("Client could not cleanup voice connection properly:", e)
        else:
            _LOGGER.success("Client successfully cleaned-up voice connection.")

    async def create_queue(self, ctx: commands.Context) -> Queue:
        _LOGGER.info(f"Client is creating a new queue for guild: '{ctx.guild.name}'...")
        # ensure that the bot is not already connected (old instance not cleaned-up properly)
        guild_id = ctx.guild.id
        await self.cleanup(ctx.voice_client, guild_id)
        try:
            voice_channel = ctx.author.voice.channel
            await voice_channel.connect(
                timeout=60, reconnect=True, self_deaf=True, self_mute=False
            )
            queue = Queue(self, ctx.voice_client, ctx.channel)
            self._queues[guild_id] = queue
            _LOGGER.success("Client successfully created voice connection.")
            return queue
        except Exception as e:
            _LOGGER.exception(
                "Client encountered and exception with voice connection:", e
            )
            await self.cleanup(ctx.voice_client, guild_id)

    async def get_queue(self, ctx: commands.Context) -> Queue:
        _LOGGER.info(f"Client is getting queue for guild: '{ctx.guild.name}'...")
        guild_id = ctx.guild.id
        if guild_id in self._queues.keys():
            _LOGGER.info(
                f"Queue for guild: '{ctx.guild.name}' does exist, returning it."
            )
            return self._queues[guild_id]
        else:
            _LOGGER.info(
                f"Queue for guild: '{ctx.guild.name}' doesn't exist, creating it."
            )
            return await self.create_queue(ctx)
