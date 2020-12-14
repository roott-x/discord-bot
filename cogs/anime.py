import discord
from discord.ext import commands
from discord.ext.commands import Bot
import spice_api
import re
import html

class Anime:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context = True)
    async def anime2(self, ctx, *args):
        MALaccount = spice_api.init_auth("project99discord","uixnDMv7LqUv")
        arg_str = ' '.join(args)
        anime = spice_api.search(arg_str,spice_api.get_medium("anime"), MALaccount)
        first_result = anime[0]
        embed = discord.Embed(title="Anime", description=first_result.title, color=0x0083d6)
        embed.set_author(name="MyAnimeList Search", icon_url="https://myanimelist.cdn-dena.com/img/sp/icon/apple-touch-icon-256.png")
        embed.set_thumbnail(url=first_result.image_url)
        embed.add_field(name="Score", value=first_result.score)
        embed.add_field(name="Status", value=first_result.status)
        if first_result.dates[1] == '0000-00-00':
            embed.add_field(name="Type", value=first_result.anime_type)
            embed.add_field(name="Episodes", value='?')
            embed.add_field(name="Start Date", value=first_result.dates[0])
            embed.add_field(name="End Date", value='?')
        else:
            embed.add_field(name="Type", value=first_result.anime_type)
            embed.add_field(name="Episodes", value=first_result.episodes)
            embed.add_field(name="Start Date", value=first_result.dates[0])
            embed.add_field(name="End Date", value=first_result.dates[1])

        def remove_html_tags(data):
            p = re.compile(r'<.*?>')
            return p.sub('', data)

        syn = remove_html_tags(html.unescape(first_result.synopsis))
        embed.add_field(name="Synopsis", value=syn, inline=False)
        embed.set_footer(text="Powered by MyAnimeList and the Spice API Wrapper")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Anime(client))
