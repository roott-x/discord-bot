import discord
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, MissingPermissions

class Role(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def join(self, ctx, *args):
        arg_str = ' '.join(args)
        file = open("docs/selfRoleDict.txt","r")
        lines = file.readlines();
        dict = eval(lines[0])
        file.close()
        role = discord.utils.get(ctx.guild.roles, name = arg_str)

        if arg_str in dict[str(ctx.guild.id)]:
            if role in ctx.author.roles:
                embed = discord.Embed(title="You have already joined this role.", color=0xf03950)
                await ctx.send(embed=embed)
            else:
                await ctx.message.author.add_roles(role)
                embed = discord.Embed(title="You have joined the " + arg_str + " role.", color=0xf03950)
                await ctx.send(embed=embed)
        else:
            if role in ctx.guild.roles:
                embed = discord.Embed(title="You do not have permission to join this role.", color=0xf03950)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="That role does not exist.", color=0xf03950)
                await ctx.send(embed=embed)

    @commands.command(pass_context = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def leave(self, ctx, *args):
        arg_str = ' '.join(args)
        role = discord.utils.get(ctx.message.guild.roles, name=arg_str)
        if role in ctx.message.guild.roles:
            if role in ctx.author.roles:
                file = open("docs/memberJoinRoleDict.txt","r")
                lines = file.readlines();
                dict = eval(lines[0])
                file.close()

                try:
                    dict_role = dict[str(ctx.message.guild.id)]
                    if arg_str == dict_role:
                        embed = discord.Embed(title="This is a default role. Contact an administrator if you want this role removed.", color=0xf03950)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.author.remove_roles(discord.utils.get(ctx.guild.roles, name = arg_str))
                        embed = discord.Embed(title="You have left the " + arg_str + " role.", color=0xf03950)
                        await ctx.send(embed=embed)
                except:
                    await ctx.author.remove_roles(discord.utils.get(ctx.guild.roles, name = arg_str))
                    embed = discord.Embed(title="You have left the " + arg_str + " role.", color=0xf03950)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="You do not have this role.", color=0xf03950)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="That role does not exist.", color=0xf03950)
            await ctx.send(embed=embed)


    @commands.command(pass_context = True)
    @has_permissions(administrator=True)
    async def setjoinrole(self, ctx, *args):
        arg_str = ' '.join(args)
        if discord.utils.get(ctx.message.guild.roles, name=arg_str) in ctx.message.guild.roles:
            file = open("docs/memberJoinRoleDict.txt","r")
            lines = file.readlines();
            dict = eval(lines[0])
            file.close()

            dict[str(ctx.message.guild.id)] = arg_str

            file = open("docs/memberJoinRoleDict.txt","w")
            file.truncate(0)
            file.write(str(dict))
            file.close
            await ctx.send(arg_str + " set as default role. When new members join, they will get this role.")
        else:
            await ctx.send("That role does not exist.")

    @commands.command(pass_context = True)
    @has_permissions(administrator=True)
    async def deljoinrole(self, ctx, *args):
        arg_str = ' '.join(args)
        if discord.utils.get(ctx.message.guild.roles, name=arg_str) in ctx.message.guild.roles:
            file = open("docs/memberJoinRoleDict.txt","r")
            lines = file.readlines();
            dict = eval(lines[0])
            file.close()

            if dict.get(str(ctx.message.guild.id), 0) != 0:
                dict.pop(str(ctx.message.guild.id))

                file = open("docs/memberJoinRoleDict.txt","w")
                file.truncate(0)
                file.write(str(dict))
                file.close
                await ctx.send(arg_str + " no longer set as default role. When new members join, they will no longer get this role.")
            else:
                await ctx.send("That role does not exist, or was not set as the default role.")
        else:
            await ctx.send("That role does not exist, or was not set as the default role.")

    @commands.command(pass_context = True, aliases = ['asr'])
    @has_permissions(administrator=True)
    async def addselfrole(self, ctx, *args):
        arg_str = ' '.join(args)
        role = discord.utils.get(ctx.message.guild.roles, name=arg_str)
        if role in ctx.guild.roles:
            file = open("docs/selfRoleDict.txt","r")
            lines = file.readlines();
            dict = eval(lines[0])
            file.close()

            if dict.get(str(ctx.message.guild.id), 0) != 0:
                list = dict[str(ctx.guild.id)]
                if arg_str in list:
                    embed = discord.Embed(title="This role is already a self assignable role.", color=0xf03950)
                    await ctx.send(embed=embed)
                else:
                    dict[str(ctx.guild.id)].append(arg_str)
                    embed = discord.Embed(title=""+arg_str+" role can now be obtained through -join.", color=0xf03950)
                    await ctx.send(embed=embed)
            else:
                dict[str(ctx.guild.id)] = [arg_str]
                embed = discord.Embed(title=""+arg_str+" role can now be obtained through -join.", color=0xf03950)
                await ctx.send(embed=embed)

            file = open("docs/selfRoleDict.txt","w")
            file.truncate(0)
            file.write(str(dict))
            file.close
        else:
            embed = discord.Embed(title="That role does not exist.", color=0xf03950)
            await ctx.send(embed=embed)

    @commands.command(pass_context = True, aliases = ['dsr'])
    @has_permissions(administrator=True)
    async def delselfrole(self, ctx, *args):
        arg_str = ' '.join(args)
        file = open("docs/selfRoleDict.txt","r")
        lines = file.readlines();
        dict = eval(lines[0])
        file.close()

        list = dict[str(ctx.guild.id)]

        if arg_str in list:
            list.remove(arg_str)
            dict[str(ctx.guild.id)] = list
            embed = discord.Embed(title=""+arg_str+" role is no longer a self assignable role.", color=0xf03950)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="This role is currently not a self assignable role.", color=0xf03950)
            await ctx.send(embed=embed)

        file = open("docs/selfRoleDict.txt","w")
        file.truncate(0)
        file.write(str(dict))
        file.close

    @commands.command(pass_context = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rolelist(self, ctx):
        file = open("docs/selfRoleDict.txt","r")
        lines = file.readlines();
        dict = eval(lines[0])
        file.close()

        try:
            list = dict[str(ctx.guild.id)]

            if (len(list) == 0):
                embed = discord.Embed(title="There are currently no self-assignable roles.", color=0x23272A)
                await ctx.send(embed=embed)
            else:

                desc = ""

                for i in list:
                    desc = desc + "\n" + i

                embed = discord.Embed(title="Self-assignable roles:", description=desc, color=0x23272A)
                await ctx.send(embed=embed)

        except:
            embed = discord.Embed(title="There are currently no self-assignable roles.", color=0x23272A)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Role(client))

#old code
'''
guild = ctx.message.author.guild
member = discord.utils.get(guild.roles, name="Member")
if member in ctx.message.author.roles:
    if discord.utils.get(guild.roles, name = arg_str) in guild.roles:
        role = discord.utils.get(guild.roles, name = arg_str)
        if role == discord.utils.get(guild.roles, name = "NSFW Permission"):
            embed = discord.Embed(title="Please ask a moderator for this role.", color=0xf03950)
            await ctx.send(embed=embed)
        else:
            if role.position >= member.position:
                embed = discord.Embed(title="You do not have permission to join this role.", color=0xf03950)
                await ctx.send(embed=embed)
            else:
                await ctx.message.author.add_roles(discord.utils.get(guild.roles, name = arg_str))
                embed = discord.Embed(title="You have joined the " + arg_str + " role.", color=0xf03950)
                await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error: Role not found.", color=0xf03950)
        await ctx.send(embed=embed)
else:
    embed = discord.Embed(title="You do not have permission to join this role.", color=0xf03950)
    await ctx.send(embed=embed)
'''
