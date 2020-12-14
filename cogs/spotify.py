import discord
from discord.ext import commands
from discord.ext.commands import Bot
import spotipy
import spotipy.oauth2 as oauth2

class Spotify(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context = True, aliases = ['sp'])
    async def spotify(self, ctx, *args):
        credentials = oauth2.SpotifyClientCredentials(client_id='spotify-client-id-here', client_secret='spotify-client-secret-here')
        token = credentials.get_access_token()
        spotify = spotipy.Spotify(auth=token)
        arg_str = ' '.join(args)
        try:
            results = spotify.search(q=arg_str, type='track', limit='1')
            link = results['tracks']['items'][0]['external_urls']['spotify']
            await ctx.send(link)
        except:
            await ctx.send('There was an error loading the track.')

def setup(client):
    client.add_cog(Spotify(client))
