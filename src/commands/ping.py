from discord.ext import commands

from lib.logger import _LOGGER


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        _LOGGER.info(
            f"User: '{ctx.author.name}' from guild: '{ctx.guild.name}' used 'play' command in '#{ctx.channel.name}'."
        )
        await ctx.reply("Pong !")
