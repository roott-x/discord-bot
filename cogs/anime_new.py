import discord
from discord.ext import commands
from discord.ext.commands import Bot
from Pymoe import Anilist
import re
import html

instance = Anilist()

class Anime(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context = True, aliases = ['a'])
    async def anime(self, ctx, *args):

        arg_str = ' '.join(args)

        #Initialize Anime Search
        ani_search = instance.search.anime(arg_str)
        ani_id = ani_search['data']['Page']['media'][0]['id']
        ani_dict = instance.get.anime(ani_id)

        #Anime Statistics
        ani_name = ani_dict['data']['Media']['title']['romaji']
        ani_image = ani_dict['data']['Media']['coverImage']['large']
        ani_ep = ani_dict['data']['Media']['episodes']
        ani_genre = ', '.join(ani_dict['data']['Media']['genres'])
        ani_syn = ani_dict['data']['Media']['description']

        #ani_format
        ani_format = ani_dict['data']['Media']['format']
        if ani_format == 'tv_short' or ani_format == 'TV_SHORT':
            ani_format = 'TV Short'
        else:
            pass

        #Status
        ani_status = ani_dict['data']['Media']['status']
        if ani_status == 'FINISHED':
            ani_status = 'Finished'
        elif ani_status == 'RELEASING':
            ani_status = 'Airing'
        elif ani_status == 'NOT_YET_RELEASED':
            ani_status = 'Unreleased'
        else:
            pass

        #Score
        ani_score = ani_dict['data']['Media']['averageScore']
        if ani_score == 'None':
            ani_score = 'Unknown'
        else:
            ani_score = str(ani_score) + ' / 100'

        #Season
        ani_season = ani_dict['data']['Media']['season']
        if ani_season == None:
            ani_season = 'None'
        else:
            ani_season = ani_season.lower()
            ani_season = ani_season.title() + ' ' + str(ani_dict['data']['Media']['startDate']['year'])

        embed = discord.Embed(title=ani_name, color=0x0083d6, url='https://anilist.co/anime/' + str(ani_id))
        embed.set_thumbnail(url=ani_image)
        embed.add_field(name="Format", value=ani_format)
        embed.add_field(name="Episodes", value=ani_ep)
        embed.add_field(name="Status", value=ani_status)
        embed.add_field(name="Season", value=ani_season)
        embed.add_field(name="Average Score", value=ani_score)
        embed.add_field(name="Genres", value=ani_genre)

        def remove_html_tags(data):
            p = re.compile(r'<.*?>')
            return p.sub('', data)

        syn = remove_html_tags(html.unescape(ani_syn))
        if len(syn) >= 1024:
            syn = syn[:1021] + '...'

        embed.add_field(name="Synopsis", value=syn, inline=False)
        embed.set_footer(text="Powered by AniList.")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Anime(client))
