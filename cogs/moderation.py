import discord
from discord import Member
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, MissingPermissions

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context = True, aliases = ['yuki'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx, *args):
        args_str = ' '.join(args)
        if args_str == 'mod':
            embed = discord.Embed(Title="Moderation Commands", description="**Moderation Commands**")
            embed.add_field(name="-kick <user>", value="Kicks the mentioned user. User must have the permissions to kick and manage roles.\n")
            embed.add_field(name="-ban <user>", value="Bans the mentioned user. User must have the permissions to ban and manage roles.\n")
            embed.add_field(name="-setjoinrole <role name>", value="Sets the role as default role that new members would receive upon joining. Role name must be spelled exactly as it is in the server settings, and must be created prior to this command's use. Requires administrator priviliges.\n")
            embed.add_field(name="-deljoinrole <role name>", value="Disables the default role function. Only works if there is a command set as a default role. Role name must be spelled exactly as it is in the server settings. Requires administrator priviliges.\n")
            embed.add_field(name="-clear <amount>", value="Clears <amount> messages. This includes the command being called. If no amount of messages is specified, the command will default to clearing 5 messages. Only 100 messages (that are under 14 days old) can be cleared at a time. Cooldown: 5s. Requires permission to delete messages. Aliases - c \n")
            await ctx.send(embed=embed)
        elif args_str == 'music':
            embed = discord.Embed(Title="Music Commands", description="**Music Commands**")
            embed.add_field(name="-connect", value="Signals Yukinon to establish a connection to a voice channel. User must be in a voice channel prior to command use in order for the connection to be established.\n")
            embed.add_field(name="-play <query>",value="Plays audio from requested query (can be a link). If Yukinon does not play anything, the site that hosts the link may not be supported. If audio is already playing, the request will be queued.\n")
            embed.add_field(name="-stop",value="Stops the audio.")
            embed.add_field(name="-pause",value="Pauses audio.")
            embed.add_field(name="-resume",value="Resumes audio.")
            embed.add_field(name="-queue",value="Shows up to 10 songs waiting to be played.")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(Title="Basic Commands", description="**Basic Commands**")
            embed.add_field(name="-help (query)", value="Brings up this menu. Optional arguments (mod, music) bring up the respective command lists for requested category.\n")
            embed.add_field(name="-anime <query>", value="Searches AniList for query. If the anime is not found, Yukinon will not return anything. Aliases - a \n ")
            embed.add_field(name="-manga", value=":soontm: \n ")
            embed.add_field(name="-wiki <query>", value="Searches Wikipedia for query. If nothing is found for that query, Yukinon will not return anything. \n ")
            embed.add_field(name="-youtube <query>", value="Searches Youtube for query and returns first result. If nothing is found for that query, Yukinon will not return anything. Aliases - yt \n")
            embed.add_field(name="-spotify <song>", value="Searches Spotify for song and returns first result. If nothing is found for that query, Yukinon will not return anything. Aliases - sp \n")
            embed.add_field(name="-avatar <user>", value="Returns the requested user's avatar. Must be a mention/ping. \n")
            embed.add_field(name="-join <role>", value ="Adds requested role to user. Parameter must be the same (including caps) as role name.\nAs of now, requestable roles are [Vote Reminders, Event Reminders]")
            embed.add_field(name="-rolelist", value="Returns list of roles that user can add through -join <role>.")
            embed.add_field(name="-mc <query>", value ="Quick links the Minecraft wiki. Queries must be spelled correctly or have the right name, or the page returned will be an error.\n")
            embed.set_footer(text="Project Yukinoshita - Built by roott#2447 on discord.py/ext rewrite ver.")
            #embed.add_field(name="-leave <role>") GET ON THIS
            await ctx.send(embed=embed)

    #kick members - no reason input
    @commands.command(name="kick", pass_context=True)
    @has_permissions(manage_roles=True, kick_members=True)
    async def _kick(self, ctx, member: Member):
        try:
            await member.kick()
            embed = discord.Embed(title="", description= "" + member.mention + " has been kicked by " + ctx.message.author.mention)
            await ctx.send(embed=embed)
        except:
            if member.top_role == ctx.message.author.top_role:
                embed = discord.Embed(Title='You cannot kick members in the same role hierarchy.')
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(Title='Failed to excecute command. Check permissions.')
                await ctx.send(embed=embed)

    #ban members - no reason input
    @commands.command(name="ban", pass_context=True)
    @has_permissions(manage_roles=True, ban_members=True)
    async def _ban(self, ctx, member: Member):
        try:
            await member.ban()
            embed = discord.Embed(title="", description= "" + member.mention + " has been banned by " + ctx.message.author.mention)
            await ctx.send(embed=embed)
        except:
            if member.top_role == ctx.message.author.top_role:
                embed = discord.Embed(Title='You cannot kick members in the same role hierarchy.')
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(Title='Failed to excecute command. Check permissions.')
                await ctx.send(embed=embed)

    @commands.command(name="clear", pass_context=True, aliases = ['c'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        if amount > 100:
            await ctx.send('I can only delete up to 100 messages. Please enter a smaller number.')
        else:
            channel = ctx.channel
            messages = []
            amount_int = int(amount)
            async for message in channel.history(limit=amount_int):
                messages.append(message)
            await channel.delete_messages(messages)
            embed = discord.Embed(title="I have deleted "+str(amount)+" messages.", color=0xf03950)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Moderation(client))
