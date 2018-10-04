import sys
import traceback
import asyncio
import logging
import discord
from discord.ext import commands
from utils import config

logging.basicConfig(level=logging.INFO)

description = 'PoroBot is an API wrapper for the Riot API, using Discord as an interface.'
cogs = [
    'cogs.base',
    'cogs.loldata'
]
bot = commands.Bot(command_prefix='-', description=description)  # Instantiate
bot.remove_command('help')


@bot.event
async def on_ready():
    print('==='*20)
    print('BOT ONLINE')
    print(
        f'LOGGED IN AS: {bot.user.name} WITH ID: {bot.user.id}')
    print('==='*20)


@bot.command(name='hey')
async def say_hey(ctx):
    await ctx.send(f'@{ctx.message.author} Hello')


@bot.command(name='reloadcog')
async def reload_cog(ctx, incog):
    bot.unload_extension(f'cogs.{incog}')
    print(f'{incog} removed.')
    bot.load_extension(f'cogs.{incog}')
    print(f'{incog} reloaded.')

if __name__ == '__main__':
    for cog in cogs:
        try:
            bot.load_extension(cog)
        except Exception as e:
            print(f'Failed to load cog {cog}.', file=sys.stderr)
            traceback.print_exc()

bot.run(config.keys['dc_bot_secret'])
