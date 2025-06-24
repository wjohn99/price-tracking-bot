from discord.ext import commands
from dotenv import load_dotenv
from price_tracking import PriceTracking
from datetime import datetime
import discord
import os
import asyncio
import sys

load_dotenv()
BOT_TOKEN = os.environ['BOT_TOKEN']

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())
price_tracking = PriceTracking()

@bot.event
async def on_ready():
    print(f'[{datetime.now().strftime("%H:%M:%S")}] Bot ready')
    if not hasattr(bot, 'nickname_task_started'):
        bot.loop.create_task(change_nickname())
        bot.nickname_task_started = True
    await bot.change_presence(
        activity=discord.Game(
            name='pvp.trade/join/opium'
        )
    )

@bot.command()
async def pvp(ctx):
    await ctx.send('https://pvp.trade/join/opium')

async def change_nickname():
    price_5m_ago = 0
    await bot.wait_until_ready()

    while not bot.is_closed():
        icon = ['(↗)', '(↘)', '(→)']
        price = price_tracking.get_coin_price(coin_id='hyperliquid')
        if price == None:
            print('Error caught: Shutting down bot')
            await bot.close()
            sys.exit()

        if price_5m_ago == 0:
            icon = icon[2]
        elif price == price_5m_ago:
            icon = icon[2]
        elif price > price_5m_ago:
            icon = icon[0]
        elif price < price_5m_ago:
            icon = icon[1]

        for guild in bot.guilds:
            try:
                await guild.me.edit(nick=f'${price:.2f} {icon}')
                print(f'[{datetime.now().strftime("%H:%M:%S")}] Changed name to ${price:.2f} {icon} in {guild.name}')
            except Exception:
                print(f'[{datetime.now().strftime("%H:%M:%S")}] Failed to change nickname in {guild.name}: {Exception}')
        price_5m_ago = price
        await asyncio.sleep(300)

bot.run(BOT_TOKEN)