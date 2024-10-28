from discord.ext import commands

from lib.logger import _LOGGER
from models.bot import Tavernier

FFMPEG_OPTIONS = {"options": "-vn"}  # Audio-only options for ffmpeg


class Play(commands.Cog):
    def __init__(self, bot: Tavernier):
        self.bot = bot

    @commands.command(name="play", aliases=["p"])
    async def play(self, ctx: commands.Context, *, url_or_title: str) -> None:
        _LOGGER.info(
            f"User: '{ctx.author.name}' from guild: '{ctx.guild.name}' used 'play' command in '#{ctx.channel.name}'."
        )
        if ctx.author.voice is None:  # Check if user is in a voice channel
            await ctx.send("You need to be in a voice channel to use this command!")
            _LOGGER.error("User is not in voice channel.")
            return

        try:
            queue = await self.bot.get_music_manager.get_queue(ctx)
            await queue.play(url_or_title)
        except Exception as e:
            _LOGGER.exception("Error while playing the song:", e)
