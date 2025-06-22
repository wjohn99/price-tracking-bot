from discord.ext import commands
from dotenv import load_dotenv
import discord
import os

load_dotenv()
BOT_TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = 1386446532328427662

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())

@bot.event
async def on_ready():
    for i in range(1):
        print('hi')
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send('hi')

@bot.command()
async def hello(ctx):
    await ctx.send('hi')

@bot.command()
async def add(ctx, *arr):
    result = 0  
    for i in arr:
        result += int(i)
    await ctx.send(f'Result: {result}')

bot.run(BOT_TOKEN)