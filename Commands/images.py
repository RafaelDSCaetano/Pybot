from discord.ext import commands


class Images(commands.Cog):
    """work with images"""

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Images(bot))