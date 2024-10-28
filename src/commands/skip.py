from discord.ext import commands

from lib.logger import _LOGGER
from models.bot import Tavernier

FFMPEG_OPTIONS = {"options": "-vn"}  # Audio-only options for ffmpeg


class Skip(commands.Cog):
    def __init__(self, bot: Tavernier):
        self.bot = bot

    @commands.command(name="skip", aliases=["s", "next", "n"])
    async def skip(self, ctx: commands.Context) -> None:
        _LOGGER.info(
            f"User: '{ctx.author.name}' from guild: '{ctx.guild.name}' used 'skip' command in '#{ctx.channel.name}'."
        )
        if ctx.author.voice is None:  # Check if user is in a voice channel
            await ctx.send("You need to be in a voice channel to use this command!")
            _LOGGER.error("User is not in voice channel.")
            return

        try:
            queue = await self.bot.get_music_manager.get_queue(ctx)
            await queue.handle_next()
        except Exception as e:
            _LOGGER.exception("Error while playing the song:", e)
