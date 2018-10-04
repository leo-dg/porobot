import time
import discord
from discord.ext import commands


class Base():
    """
    This class contains basic functionality for PoroBot.
    """

    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        channel = message.channel

        if message.content.startswith('-hello'):
            await channel.send(
                "hey dude!")
        elif message.content.startswith('-ping'):
            st = time.time()
            response = await channel.send('Ping!')

            await response.edit(content=f'Pong! _{int((time.time() - st)*100)}ms_')

        # await self.bot.process_commands(message)

    @commands.command(name='help')
    async def display_help(self, ctx):
        '''
        Sends an embed message containing the commands for PoroBot.
        '''

        # Define the embed.
        emb = discord.Embed(
            title="Help",
            description="Here's a list of commands! owo~",
            colour=discord.Colour.dark_blue()
        )
        emb.set_thumbnail(
            url='http://ddragon.leagueoflegends.com/cdn/7.5.1/img/sticker/poro-question.png')
        emb.add_field(
            name='-ping', value='Find out your KDR on Black Ops 1!', inline=False)
        emb.add_field(name='-userinfo _username_',
                      value='Get data about a summoner and their previous match.')
        emb.add_field(name='-iteminfo _item name_',
                      value='Find out about a certain item.')

        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Base(bot))
