import discord
from discord.ext import commands
from discord.ext.commands import Bot

class Minecraft(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context = True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def mc(self, ctx, *args):
        arg_str = '_'.join(args)
        await ctx.send("https://minecraft.gamepedia.com/" + arg_str)

def setup(client):
    client.add_cog(Minecraft(client))
