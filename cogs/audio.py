import asyncio
import discord
import youtube_dl
from async_timeout import timeout
from discord.ext import commands

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'music/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

if not discord.opus.is_loaded():
    discord.opus.load_opus()

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class VoiceState:
    def __init__(self, ctx):
        self.ctx = ctx
        self.client = ctx.bot
        self.channel = ctx.channel
        self.queue = []
        self.voice = ctx.voice_client
        self.songs = asyncio.Queue()
        self.play_next_song = asyncio.Event()
        self.now_playing = ""

        self.client.loop.create_task(self.audio_player_task())

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            try:
                async with timeout(500):
                    current = await self.songs.get()
                    embed = discord.Embed(title="Now playing: {}".format(current.title), color=0x67e571)
                    await self.channel.send(embed=embed)
                    #await self.channel.send('Now playing: {}'.format(current.title))
                    self.queue.pop()[0]
                    self.now_playing = current.title
                    self.voice.play(current, after=lambda x: self.client.loop.call_soon_threadsafe(self.play_next_song.set))
                    await self.play_next_song.wait()
                    current.cleanup()
            except asyncio.TimeoutError:
                await self.voice.disconnect()
                self.now_playing = ""
                self.queue = []

class Audio(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.voices = {}

    @commands.command(pass_context=True, aliases=['connect'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def connect_(self, ctx):
        if ctx.author.voice:
            try:
                ctx.voice_client.pause()
            except:
                pass

            try:
                await ctx.voice_client.disconnect()
            except:
                pass

            await ctx.author.voice.channel.connect()

            state = VoiceState(ctx)
            self.voices[ctx.guild.id] = state
            #print('Created new voice client')

            try:
                ctx.voice_client.resume()
            except:
                pass

            await ctx.send('Connected to channel.')
        else:
            await ctx.send("You are not connected to a voice channel.")

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def play(self, ctx, *, url):
        player = await YTDLSource.from_url(url, loop=self.client.loop)
        if ctx.voice_client.is_playing():
            await ctx.send('Since there is a song playing, I have queued your request.')
        await self.voices[ctx.guild.id].songs.put(player)
        self.voices[ctx.guild.id].queue.append(player.title)

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        self.voices[ctx.guild.id].songs = asyncio.Queue()
        self.voices[ctx.guild.id].now_playing = ""
        self.voices[ctx.guild.id].queue = []
        await ctx.voice_client.disconnect()

    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def pause(self, ctx):
        if ctx.voice_client.is_paused():
            await ctx.send('I have already paused the audio.')
        else:
            ctx.voice_client.pause()
            await ctx.send('I have paused the audio.')

    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def resume(self,ctx):
        if ctx.voice_client.is_playing():
            await ctx.send('I am already playing audio. Is your head alright?')
        else:
            ctx.voice_client.resume()
            await ctx.send('I have resumed the audio.')

    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def queue(self, ctx):
        embed = discord.Embed(Title='Music Queue for ' + ctx.guild.name + ' in ' + ctx.channel.name, description="Music Queue for " + ctx.guild.name + ' through #' + ctx.channel.name)
        embed.add_field(name="**[Now Playing]**", value=""+self.voices[ctx.guild.id].now_playing)
        titles = []
        if (len(self.voices[ctx.guild.id].queue) > 10):
            titles = self.voices[ctx.guild.id].queue[:10]
        else:
            titles = self.voices[ctx.guild.id].queue

        i = 1

        for title in titles:
            embed.add_field(name="["+str(i)+"]", value=title)
            i+=1

        await ctx.send(embed=embed)

    @play.before_invoke
    @pause.before_invoke
    @resume.before_invoke
    @stop.before_invoke
    @queue.before_invoke
    async def not_in_voice(self, ctx):
        if ctx.voice_client is None:
            await ctx.send("I am not connected to a voice channel. Use -connect when in a voice channel to instruct me to join.")

def setup(client):
    client.add_cog(Audio(client))
