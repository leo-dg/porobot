import discord
from discord.ext import commands
from utils import requests


class Loldata():
    """
    DATA INPUT FROM Riotwrapper
    OUTPUT TO DISCORD VIA Embed
    """

    def __init__(self, bot):
        self.bot = bot
        self.interface = requests.Riotwrapper()

    @commands.command(name='getstatus')
    async def display_status(self, ctx):
        '''
        Sends the status for EUW game, client, store and web. TODO: Implement multi-region
        '''
        statuses = self.interface.get_status()  # Object storing all statuses.

        def status_light(component_status):
            return ':large_blue_circle:' if component_status == 'online' else ':red_circle:'

        emb = discord.Embed(
            title=f'Riot Services {statuses["region"]}',
            description="Check the status of Riot's services.",
            colour=discord.Colour.dark_blue()
        )
        emb.set_thumbnail(
            url='http://ddragon.leagueoflegends.com/cdn/7.5.1/img/sticker/poro-shock.png'
        )
        emb.add_field(
            name='Game',
            value=f'Status: {statuses["game_status"]} {status_light(statuses["game_status"])}'
        )
        emb.add_field(
            name='Client',
            value=f'Status: {statuses["client_status"]} {status_light(statuses["client_status"])}'
        )
        emb.add_field(
            name='Store',
            value=f'Status: {statuses["store_status"]} {status_light(statuses["store_status"])}'
        )
        emb.add_field(
            name='Website',
            value=f'Status: {statuses["web_status"]} {status_light(statuses["web_status"])}'
        )

        await ctx.send(embed=emb)

    @commands.command(name='userinfo')
    async def display_user_info(self, ctx, user):
        # TODO: ==> Validation <==
        user_info = self.interface.get_user_info(user)
        if user_info == -1:
            await ctx.send(f"Error: Summoner _{user}_ does not exist!")
            return
        lmatch_info = self.interface.get_lastmatch_info(user_info['user_id'])
        champ_data = self.interface.get_champ(lmatch_info["champ"])

        emb = discord.Embed(
            title=f"Summoner Info - {user}",
            description=f"Here's some data about summoner {user}.",
            colour=discord.Colour.dark_blue()
        )
        emb.set_thumbnail(
            url=user_info['pfp_url']
        )

        emb.add_field(
            name='Username',
            value=user_info['user_name']
        )

        emb.add_field(
            name='Summoner Level',
            value=user_info['user_level']
        )

        emb.add_field(
            name='Matches Played',
            value=lmatch_info['match_count']
        )

        # Last Match Embed
        emb2 = discord.Embed(
            title=f"Last Match Info - {user}",
            color=discord.Colour.dark_blue()
        )

        emb2.set_thumbnail(
            url=champ_data["champ_pfp_url"])

        emb2.add_field(
            name='Map',
            value=lmatch_info['map']
        )

        emb2.add_field(
            name='Result',
            value=lmatch_info['result']  # **
        )

        emb2.add_field(
            name='Champion',
            value=champ_data["name"])

        emb2.add_field(
            name='Lane',
            value=lmatch_info['lane']
        )

        emb2.add_field(
            name='Role',
            value=lmatch_info['role']
        )

        emb2.add_field(
            name="Kills | Deaths | Assists",
            value=lmatch_info['kda']
        )

        await ctx.send(embed=emb)
        await ctx.send(embed=emb2)


def setup(bot):
    bot.add_cog(Loldata(bot))
