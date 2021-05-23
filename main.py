from os import environ

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
bot.load_extension('generator_cog')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'Version: {discord.__version__}')


bot.run(environ.get('DISCORD_BOT_TOKEN'), bot=True, reconnect=True)
