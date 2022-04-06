from discord.ext import commands


class Reaction(commands.Cog):
    """work with reactions"""

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Reaction(bot))