from .cogs import DogCog
from discord.ext import commands


async def setup(bot: commands.Bot):
    await bot.add_cog(DogCog(bot))