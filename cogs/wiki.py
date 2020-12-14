import discord
from discord.ext import commands
from discord.ext.commands import Bot
import wikipedia

class Wiki(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context = True)
    async def wiki(self, ctx, *args):
        args_str = ' '.join(args)
        args_str2 = '_'.join(args)
        try:
            wiki = wikipedia.page(args_str)
        except:
            await ctx.send("Looks like I couldn't find a specific page.")
            await ctx.send("Here's a reference you might use: https://en.wikipedia.org/wiki/" + args_str2)
        summary = wikipedia.summary(args_str, sentences=3)
        embed = discord.Embed(title=wiki.title, description=summary, url=wiki.url, color=0xffffff)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Wiki(client))
