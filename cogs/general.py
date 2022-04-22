import discord
from discord.ext import commands
import asyncio
from googlesearch import search
from text_to_num import text2num
import urllib
import re
from urllib.request import urlopen
from . import cmodule
from . import doggo

text = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = 'X won!'
            elif winner == view.O:
                content = 'O won!'
            else:
                content = "It's a tie!"

            for child in view.children:
                assert isinstance(child, discord.ui.Button)
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(discord.ui.View):
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

class Fun(commands.Cog):
    """Random Commands that are mostly useless"""

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def howlong(self, ctx, age):
        """Atom will try and estimate your lifespan"""
        url = 'https://www.singstat.gov.sg/find-data/search-by-theme/population/death-and-life-expectancy/latest-data'
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")
        pattern = '<td style="text-align: center; background-color: white;">&nbsp;.*?</td>'
        match_results = re.search(pattern, html, re.IGNORECASE)
        d = match_results.group()
        data = re.sub("<.*?>", "", d)
        tl = data.strip('&nbsp;')
        lx = float(tl) - int(age)
        alx = str(lx)
        await ctx.send('You have roughly ' + alx + ' years left to live')

    @commands.command()
    async def google(self, ctx, *args):
        """Searches the internet"""
        async with ctx.typing():
            query = (" ".join(args[:]))
            ggl = search(query, tld="co.in", num=4, stop=4, pause=2)
            j1, j2, j3, j4 = ggl
            embed = discord.Embed(title=f'Google Search for  ```{query}```',
                                  description='These are the top 4 results I could find:')
            embed.add_field(name='Result 1:', value=j1)
            embed.add_field(name='Result 2:', value=j2, inline=False)
            embed.add_field(name='Result 3:', value=j3, inline=True)
            embed.add_field(name='Result 4:', value=j4, inline=False)
            embed.set_footer(text="Don't like the results? do !feedback to help us out")
        await ctx.send(embed=embed)

    @commands.command()
    async def trivia(self, ctx):
        """Gives Random Trivia Question"""
        await ctx.trigger_typing()
        htm = urllib.request.urlopen(url="http://old.randomtriviagenerator.com/random_pub_quiz.php")
        html = str(htm.read())

        x = re.findall(r'<td align="left">(.+?)</a></td>', html)
        y = re.findall(r'<td align="left">(.+?)</td>', html)

        qust = x[0].replace('<a href="question_a.php?q=', ' ')
        ans = str(y[1])
        question = re.sub(r'.', '', qust, count=5).replace('>', '')
        if question.startswith('"'):
            question = question.strip('"')
        if ans in text:
            data2 = text2num(ans)
        else:
            data2 = (str(ans)).lower().replace('/', '').replace('-', '').replace(" ", "")

        print(question)
        print(ans)

        embed = discord.Embed(title='Trivia Question',
                              url='http://old.randomtriviagenerator.com/random_pub_quiz.php',
                              description=f'{question}',
                              colour=0x109319
                              )
        embed.set_footer(text='Note: Only the Author can answer the question')

        await ctx.send(embed=embed)

        def check(m):
            return m.author == ctx.message.author and m.channel == ctx.message.channel
        try:
            message = await self.bot.wait_for('message', check=check, timeout=60)
            if data2.replace(" ", "") in str(message.content).lower().replace(" ", "").lower().replace('/', '').replace('-', ''):
                await ctx.send('Correct Answer!')
            else:
                await ctx.send(f'Sorry! wrong answer, the correct answer should be "{ans}" ')
        except asyncio.TimeoutError:
            await ctx.send(f'Times Up! The correct answer was "{ans}')

    @commands.command()
    async def tic(self, ctx: commands.Context):
        """Wanna play tic tac toe?"""
        await ctx.send('Tic Tac Toe: X goes first', view=TicTacToe())

    @commands.command(allias='cats')
    async def kitties(self, ctx, *args):
        """Cats are freaking adorable"""
        await ctx.trigger_typing()
        if args is None or str(args) == "()":
            url = cmodule.cat()
            embed = discord.Embed(title="You ask and you shall receive CATS",
                                  description="Here is a random picture of a cat, do =kitties (tag) to get more!",
                                  colour=0xfb0064)
            embed.set_image(url=url)
            await ctx.send(embed=embed)
        else:
            tag = ""
            for arg in args:
                tag = tag+arg+" "
            url = cmodule.cat(tag)
            if url is not False:
                embed = discord.Embed(title="You ask and you shall receive CATS",
                                      description=f"Here is an adorable cat `Tag: {str(tag)}`",
                                      colour=0xfb0064)
                embed.set_image(url=url)
                await ctx.send(embed=embed)
            else:
                url = cmodule.cat()
                embed = discord.Embed(title="Aw man",
                                      description="It seems like your query didn't bring up any results that is so sad on so many levels",
                                      colour=0xfb0064)
                embed.set_image(url=url)
                await ctx.send(embed=embed)

    @commands.command(allias='dogs')
    async def doggo(self, ctx, tag=None):
        """Dogs are cool as well i guess"""
        await ctx.trigger_typing()
        if tag is None:
            url = doggo.doggo()
            embed = discord.Embed(title="Doggos are quite splendid little creatures",
                                  description="Here is a random picture of a dog you can do =doggo (breed) to specify",
                                  colour=0xee00ff)
            embed.set_image(url=url)
            await ctx.send(embed=embed)
        else:
            url = doggo.doggo(str(tag))
            if url != "https://th.bing.com/th/id/OIP.eaohbN4jI152vWHz4v0Z0gHaHa?w=201&h=201&c=7&r=0&o=5&dpr=1.25&pid=1.7":
                embed = discord.Embed(title=f"Doggos are quite splendid little creatures",
                                      description=f"Here is one of the many {tag} dogs out there!",
                                      colour=0xee00ff)
                embed.set_image(url=url)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title=f"Perhaps the archives are incomplete...",
                                      description=f"So there are no entries in the doggo library about {tag}.. Here is another pic instead",
                                      colour=0xee00ff)
                embed.set_image(url=url)
                await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(Fun(bot))