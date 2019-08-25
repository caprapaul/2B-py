import discord
from discord.ext import commands
import utils.database as database


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='dbadd')
    async def db_add(self, ctx, user: discord.Member):
        """Force add user to database."""
        database.add_new_user(user)
        await ctx.send('Successfully')


def setup(bot):
    bot.add_cog(Moderation(bot))
