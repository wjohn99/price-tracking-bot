from discord.ext import commands
from dotenv import load_dotenv
from price_tracking import PriceTracking
import discord
import os
import asyncio

load_dotenv()
API_KEY = os.environ['API_KEY']
BOT_TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = 1386446532328427662

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())
price_tracking = PriceTracking()

@bot.event
async def on_ready():
    for i in range(1):
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send('ready')
    if not hasattr(bot, 'nickname_task_started'):
        bot.loop.create_task(change_nickname())
        bot.nickname_task_started = True

@bot.command()
async def hello(ctx):
    await ctx.send('hi')

@bot.command()
async def add(ctx, *arr):
    result = 0  
    for i in arr:
        result += int(i)
    await ctx.send(f'Result: {result}')

@bot.command()
async def hl(ctx):
    price = price_tracking.get_coin_price(coin_id='hyperliquid')
    if price:
        await ctx.send(str(price))
    else:
        await ctx.send('No price found for Hyperliquid.')

async def change_nickname():
    await bot.wait_until_ready()
    while not bot.is_closed():
        price = price_tracking.get_coin_price(coin_id='hyperliquid')
        channel = bot.get_channel(CHANNEL_ID)
        for guild in bot.guilds:
            try:
                await guild.me.edit(nick=f'HYPE@{str(price)}')
                await channel.send(f'Changed name to HYPE@{str(price)}')
            except Exception:
                print(f"Failed to change nickname in {guild.name}: {Exception}")
        await asyncio.sleep(300)

bot.run(BOT_TOKEN)