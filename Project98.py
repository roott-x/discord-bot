import discord
#pip3 install git+https://github.com/Rapptz/discord.py@rewrite
from discord import Member
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, MissingPermissions
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re
import asyncio
import html

client = commands.Bot(command_prefix='-')
client.remove_command('help')
client.load_extension('cogs.anime_new')
client.load_extension('cogs.youtube')
client.load_extension('cogs.spotify')
client.load_extension('cogs.root')
client.load_extension('cogs.wiki')
#client.load_extension('cogs.ss')
client.load_extension('cogs.role')
client.load_extension('cogs.moderation')
client.load_extension('cogs.minecraft')
client.load_extension('cogs.audio')

@client.event
async def on_ready():
    print('---------')
    print('Launching')
    print(client.user.name)
    print(client.user.id)
    print('I am ready. Are you?')
    print('---------')
    #activity = discord.Game(name="Octopath Traveler")
    #await client.change_presence(activity=activity)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("This command is on cooldown. I'd prefer if you were a bit more mature and didn't spam it.")
    elif isinstance(error, discord.ext.commands.errors.CheckFailure):
        await ctx.send("I'd prefer if someone like you didn't do that.")
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        formatter = commands.formatter.HelpFormatter()
        await ctx.send("You are missing required arguments. Can't you do anything correctly for once?")
    else:
        await ctx.send("An error occurred while processing the `{}` command.".format(ctx.command.name))

@client.command(name='reload', hidden=True)
async def _reload(ctx, *args):
    if ctx.message.author.id != owner-id-here:
        await ctx.send('Excuse me. I do not believe you have my permission to do that.')
    else:
        """Reloads a module."""
        try:
            args_str = ' '.join(args)
            client.unload_extension('cogs.' + args_str)
            client.load_extension('cogs.' + args_str)
        except Exception as e:
            await ctx.send('Ah, there seems to have been an error.')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('I have followed your request to the extent of my capabilities.')

@client.command(pass_context = True)
async def avatar(ctx):
    embed = discord.Embed(title="Avatar URL Link", url = ctx.message.mentions[0].avatar_url + "?size=2048")
    embed.set_author(name=ctx.message.mentions[0].name + "#" + ctx.message.mentions[0].discriminator)
    embed.set_thumbnail(url=ctx.message.mentions[0].avatar_url + "?size=2048")
    await ctx.send(embed=embed)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author.bot: return
    await client.process_commands(message)

@client.event
async def on_member_join(member):
    file = open("docs/memberJoinRoleDict.txt","r")
    lines = file.readlines();
    dict = eval(lines[0])
    file.close()

    try:
        guild = member.guild
        await member.add_roles(discord.utils.get(guild.roles, name=dict.get(str(guild.id))))
    except:
        pass;

client.run('BOT-TOKEN-HERE')
