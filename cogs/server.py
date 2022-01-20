import discord
from discord.ext import commands
import random
from discord.utils import get
import asyncio

class Server(commands.Cog):
    """Moderation and Administration Commands (NOTE: Most commands in this category are restricted)"""

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(hidden=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount):
        if amount is None:
            await ctx.channel.purge(limit=10)
        else:
            try:
                int(amount)
            except:
                await ctx.send('tf u want me to do, delete half a message? Enter an Integer')
            else:
                await ctx.channel.purge(limit=int(amount))

    @commands.command(hidden=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason):
        await member.send(f'You got banned from {ctx.guild.name}, reason: ```{reason}```')
        await member.ban()
        await ctx.message.delete()

    @commands.command(hidden=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member):
        await member.send(f'Kicked from {ctx.guild.name}')
        await member.kick()
        await ctx.message.delete()

    @commands.command(hidden=True)
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, time=None):
        if get(ctx.guild.roles, name="muted"):
            mt = get(ctx.guild.roles, name="muted")
        else:
            mt = await ctx.guild.create_role(name="muted", reason="To use for muting")
            for channel in ctx.guild.channels:
                await channel.set_permissions(mt, send_messages=False, connect=False)


        await member.add_roles(mt)
        await ctx.send(f"{member.mention} has been muted!")

        if time is None:
            await asyncio.sleep(60)
        else:
            time = int(time)
            try:
                await asyncio.sleep(time)
            except:
                await asyncio.sleep(60)

        await member.remove_roles(mt)



    @commands.command()
    async def userinfo(self, ctx, member: discord.Member):
        """Displays Information About Specified User"""
        channel = ctx.message.channel
        mName = member.name
        joined = member.joined_at.strftime("%d %B %Y")
        activs = list(member.activities)
        crt = member.created_at
        messages = await channel.history(limit=100).flatten()
        highest = member.top_role.name

        if str(member.desktop_status) == "online":
            dev = "Desktop"
        elif str(member.mobile_status) == "online":
            dev = "Mobile"
        elif str(member.web_status) == "online":
            dev = "Web"
        else:
            dev = "None"

        for activ in activs:
            if "ActivityType.playing" in str(activ):
                play = str(activ)
                game = (play.replace("<Activity type=<ActivityType.playing: 0> name='", '').replace(
                    "' url=None details=None application_id=356875570916753438 session_id=None emoji=None>", ''))

            if "Spotify" in str(activ):
                url = "https://open.spotify.com/track/" + activ.track_id
                title = activ.title

        aUrl = member.avatar
        rmessage = messages[random.randint(0, 100)]
        embed = discord.Embed(title=f"**User Information for {mName}:**", description=f"| [Github](https://github.com/Little-RR/atomdiscord) | [Invite](https://discord.com/api/oauth2/authorize?client_id=895668486611824650&permissions=8&scope=bot) |"
                                                                                      f"\n```{mName} Once said...  '{rmessage.content}'```", color=0x109319)
        embed.set_author(name=mName, icon_url=str(aUrl))
        embed.add_field(name="Join Date:", value=f"```{joined}```", inline=True)
        if "ActivityType.playing" in str(activs):
            print('yest')
            embed.add_field(name="Currently Playing:", value=f"```{game}```", inline=True)
        else:
            embed.add_field(name="Currently Playing:", value=f"```{None}```", inline=True)
        if "Spotify" in activs:
            embed.add_field(name="Currently Listening (Spotify):", value=f"```[{title}]({url})```", inline=True)
        else:
            embed.add_field(name="Currently Listening:", value=f"```{None}```", inline=True)
        embed.add_field(name="Created At:", value=f"```{crt.strftime('%d %B %Y')}```", inline=True)
        embed.add_field(name="Online Device:", value=f"```{dev}```", inline=True)
        embed.add_field(name="Top Role:", value=f"```{highest}\n```", inline=True)
        embed.set_footer(text=f"Requested by: {ctx.message.author}")
        await ctx.send(embed=embed)







def setup(bot):
    bot.add_cog(Server(bot))