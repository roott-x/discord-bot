import discord
from discord.ext import commands
from discord.ext.commands import Bot
import urllib.request
import urllib.parse
import re

class Youtube(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context = True, aliases = ['yt'])
    async def youtube(self, ctx, *args):
        query_string = urllib.parse.urlencode({"search_query" : args})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        arg_str = ' '.join(args)
        try:
            await ctx.send("<:YouTube:565342128864231434> | **Showing top result for: **" + arg_str)
            await ctx.send("\nhttp://www.youtube.com/watch?v=" + search_results[0])
        except:
            await ctx.send("There was an error loading the request.")

def setup(client):
    client.add_cog(Youtube(client))
