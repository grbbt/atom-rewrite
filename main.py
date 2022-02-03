import asyncio
import io
from datetime import datetime
from string import Template
import discord
import requests
from discord.ext import commands
from cogs.img import welcome
from dotenv import load_dotenv
import os



load_dotenv('.env')
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='=', intents=intents)
bot.remove_command('help')
ids = [384689131369922582, 881861488166445098]
url = 'https://raw.githubusercontent.com/Discord-AntiScam/scam-links/main/urls.json'
page = requests.get(url)
scam = page.json()


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    res = [ele for ele in scam if (ele in message.content)]
    if bool(res) is True:
        try:
            ath = message.author
            dm = await ath.create_dm()
            await message.delete()
            await dm.send('Do not post any scam links >:(')
        except:
            pass


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('The singularity bot'))
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))
    for cog in bot.cogs:
        print(f"Loaded Cog: {cog}")
    while True:
        await asyncio.sleep(10)
        with open('data.spam.txt', 'a') as a:
            a.truncate(0)



@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"You are missing the required parameter: '{error.param.name}'")
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I am afraid that I cannot do that")


@bot.event
async def on_member_join(member):
    guild = member.guild
    av = member.avatar
    if av is None:
        av = 'https://i.ibb.co/Bny0mzQ/un.jpg'
    else:
        pass
    name = member.name
    b = guild.name
    wel = await welcome(av, name, b)

    with io.BytesIO() as image_binary:
        wel.save(image_binary, 'PNG')
        image_binary.seek(0)
        file = discord.File(fp=image_binary, filename='image.png')

    embed = discord.Embed(title=f"Welcome to {b} {name}!", colour=discord.Color.dark_gold())
    embed.set_image(url="attachment://image.png")
    await guild.system_channel.send(f"Welcome {member.mention}!")
    await guild.system_channel.send(file=file, embed=embed,)


bot.load_extension('cogs.general')
bot.load_extension('cogs.server')
bot.load_extension('cogs.musiccog')
bot.load_extension('cogs.help')


@bot.command()
async def invite(ctx):
    """Sends Invite link for bot"""
    dm = await ctx.message.author.create_dm()
    embed = discord.Embed(title="Add me to your server !",
                          url="https://discord.com/api/oauth2/authorize?client_id=895668486611824650&permissions=8&scope=bot",
                          colour=0xffffff)
    await ctx.message.add_reaction(emoji='✉')
    await dm.send(embed=embed)
    await asyncio.sleep(5)
    await ctx.message.delete()


@bot.command(hidden=True)
async def hehehe(ctx, payload=None, sub=None, *args):
    """hehehe"""

    if ctx.message.author.id in ids:
        dm = await ctx.message.author.create_dm()
        if payload != None:
            try:
                await ctx.message.delete()
            except:
                pass
        if payload == None:
            await ctx.send('hehehehe')
        elif payload == 'modhelp':
            dm.send('clear, ban, kick')
        elif payload == 'shutdown':
            await dm.send('Bot Shutting Down')
            await bot.close()
        elif payload == 'test':

            await dm.send('TEST')
            embed = discord.Embed(title='TEST', description='TEST')
            await dm.send(embed=embed)

        elif payload == "save" and sub is not None:
            if sub == "write":
                try:
                    await ctx.message.delete()
                except:
                    pass
                embed = discord.Embed(title="Saved Command", description=f"`{str(' '.join(args))}`")
                await dm.send(embed=embed)
                f = open("saved.txt", "w")
                f.write(str(' '.join(args)))
        elif payload == "launch":
            print(ctx.message.author.avatar)

        elif payload == "change" and sub is not None:
            if sub != "countdown":
                changed = str(' '.join(args))
                try:
                    await ctx.message.delete()
                except:
                    pass
                await bot.change_presence(activity=discord.Game(changed))
                await asyncio.sleep(float(sub))
                await bot.change_presence(activity=discord.Game('The singularity bot'))
            else:
                var = datetime(2022, 1, 1) != datetime.now()
                while var is True:
                    tdelta = datetime(2022, 1, 1) - datetime.now()

                    class DeltaTemplate(Template):
                        delimiter = "%"

                    def strfdelta(tdelta, fmt):
                        d = {"D": tdelta.days}
                        d["H"], rem = divmod(tdelta.seconds, 3600)
                        d["M"], d["S"] = divmod(rem, 60)
                        t = DeltaTemplate(fmt)
                        return t.substitute(**d)

                    x = strfdelta(tdelta, "%D days %H:%M:%S")
                    var = bool(datetime(2022, 1, 1) != datetime.now())

                    await bot.change_presence(activity=discord.Game(x))
                    await asyncio.sleep(2.25)

                await bot.change_presence(activity=discord.Game('HAPPY NEW YEARS EVERYBODY'))
                for guild in bot.guilds:
                    for channel in guild.channels:
                        try:
                            embed = discord.Embed(title="HAPPY NEW YEARS EVERYONE",
                                                  description="Atom wishes all of you a very very happy 2022",
                                                  colour=0xe1ff00)
                            embed.set_thumbnail(url="https://i.ibb.co/j5gt4vt/Untitled.png")
                            await channel.send(ctx.message.guild.default_role)
                            await channel.send(embed=embed)
                            print(embed)
                        except Exception:
                            continue
                        else:
                            break
                await asyncio.sleep(86400)

                await bot.change_presence(activity=discord.Game('The singularity bot'))


        else:
            return None
    else:
        await ctx.send(f'I am afraid I cannot do that {ctx.message.author}')



bot.run('OTM4Nzk4MDgxODM3NzY0NjE4.Yfvh2A.NM2W2pwHoxisA1v3eYEVWM_Mlq8')
