import discord
from discord.ext import commands
from discord.ext.commands import Bot

class Root(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context = True)
    async def setgame(self, ctx, *args):
        if ctx.message.author.id != owner-id-here:
            await ctx.send('Excuse me. I do not believe you have my permission to do that.')
        else:
            args_str = ' '.join(args)
            activity = discord.Game(name = args_str)
            await self.client.change_presence(activity = activity)
            await ctx.send('It seems that I am now playing ' + args_str + '.')

    @commands.command(pass_context = True)
    async def setwatch(self, ctx, *args):
        if ctx.message.author.id != owner-id-here:
            await ctx.send('Excuse me. I do not believe you have my permission to do that.')
        else:
            args_str = ' '.join(args)
            activity = discord.Activity(name = args_str, type = discord.ActivityType.watching)
            await self.client.change_presence(activity = activity)
            await ctx.send('It seems that I am now watching ' + args_str + '.')

    @commands.command(pass_context = True)
    async def setlisten(self, ctx, *args):
        if ctx.message.author.id != owner-id-here:
            await ctx.send('Excuse me. I do not believe you have my permission to do that.')
        else:
            args_str = ' '.join(args)
            activity = discord.Activity(name = args_str, type = discord.ActivityType.listening)
            await self.client.change_presence(activity = activity)
            await ctx.send('It seems that I am now listening to ' + args_str + '.')

    @commands.command(pass_context = True)
    async def changename(self, ctx, *args):
        if ctx.message.author.id != owner-id-here:
            await ctx.send('Excuse me. I do not believe you have my permission to do that.')
        else:
            args_str = ' '.join(args)
            await self.client.user.edit(username = args_str)
            await ctx.send('I have fulfilled your request to the fullest extent of my capabilities.')

    @commands.command(name='unload', hidden=True)
    async def unload(self, ctx, *args):
        if ctx.message.author.id != owner-id-here:
            await ctx.send('Excuse me. I do not believe you have my permission to do that.')
        else:
            try:
                args_str = ' '.join(args)
                self.client.unload_extension('cogs.' + args_str)
            except Exception as e:
                await ctx.send('Ah, there seems to have been an error.')
                await ctx.send('{}: {}'.format(type(e).__name__, e))
            else:
                await ctx.send('I have followed your request to the extent of my capabilities.')

def setup(client):
    client.add_cog(Roott(client))
