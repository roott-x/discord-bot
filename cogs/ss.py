import discord
from discord.ext import commands
from discord.ext.commands import Bot

class Safe:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context = True, hidden=True)
    async def rules(self, ctx, *args):
        if ctx.message.author.id != owner-id-here:
            await ctx.send('Excuse me. I do not believe you have my permission to do that.')
        else:
            embed = discord.Embed(title="Welcome to the Safe Survival Discord server! Please take a moment to review the rules:", color=0xffffff)
            embed.set_image(url='https://cdn.discordapp.com/attachments/267773920038354944/473318998637805568/trial.png')
            await ctx.send(embed=embed)

            embed = discord.Embed(title="Rule 1", color=0xf03950, description="Please engage in conversations in a civilized manner. Be kind to your fellow members. If any drama arises here, please take it to pms. Don't cause drama for the sake of causing it. If anyone causes you trouble, contact the mods. ")
            await ctx.send(embed=embed)

            embed = discord.Embed(title="Rule 2", color=0xf5a623, description="No spam. This includes self-promotion (e.g. blatant advertisements for shops in-game) and posting invite links to other servers (e.g. other Discord/Minecraft servers).")
            await ctx.send(embed=embed)

            embed = discord.Embed(title="Rule 3", color=0xf8e71c, description="Please post all images in #memes-and-pictures. Inappropriate content is not allowed in channels other than #nsfw. If you are not sure if an image is appropriate for the channel, pm a mod first.")
            await ctx.send(embed=embed)

            embed = discord.Embed(title="Rule 4", color=0x42bb2e, description="#nsfw is a hidden channel with access granted by Moderators at their own discretion. NSFW content (text, images or otherwise) is restricted to #nsfw. However, there are lines you're still not allowed to cross in #nsfw.")
            await ctx.send(embed=embed)

            embed = discord.Embed(title="Rule 5", color=0x4787d2, description="Use @Moderator pings only when needed. If it’s easily solved with a single personal ping of a single mod that is currently online, please don’t disturb the others.")
            await ctx.send(embed=embed)

            embed = discord.Embed(title="The mods reserve the right to take corrective action if they deem your behavior inappropriate. **Check the pins if you're not sure if something is appropriate for a channel. They may include more rules.**", color=0xffffff)
            await ctx.send(embed=embed)

    @commands.command(pass_context = True, hidden=True)
    async def links(self, ctx, *args):
        if ctx.message.author.id != owner-id-here:
            await ctx.send('Excuse me. I do not believe you have my permission to do that.')
        else:
            embed = discord.Embed(title="Important Server Links")
            embed.add_field(name="Server/Forum Rules", value="https://www.safesurvival.net/pages/rules-list/")
            embed.add_field(name="Forums", value="https://www.safesurvival.net/forums/")
            embed.add_field(name="Voting Sites", value="http://mcsl.safesurvival.net/\nhttp://pmc.safesurvival.net/\nhttp://mcf.safesurvival.net/")
            embed.add_field(name="Store", value="http://store.safesurvival.net/")
            embed.add_field(name="Discord", value="https://discord.gg/vPDEkPA")
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Safe(client))
