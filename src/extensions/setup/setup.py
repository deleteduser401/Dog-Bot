from .cogs import mobileAFKModeCog, BotInfoCog
from discord.ext import commands


async def setup(bot: commands.Bot):
    await bot.add_cog(mobileAFKModeCog(bot))
    await bot.add_cog(BotInfoCog(bot))
    await bot.get_cog('BotInfoCog').setBotSettings()