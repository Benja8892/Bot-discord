from __future__ import unicode_literals
import os
from dotenv import load_dotenv

import discord
from discord.ext import commands 
from discord import app_commands
from discord import VoiceClient
from discord.utils import get
from discord import TextChannel

import asyncio
import tracemalloc

#DISCORD BOT TOKEN
load_dotenv() 
TOKEN = os.getenv("DISCORD_TOKEN")

tracemalloc.start()

#PREFIJOS DE COMANDOS TIENE QUE EMPEZAR CON /
client = commands.Bot(command_prefix="/", description='This is a helper bot',intents=discord.Intents.all())

async def load():
    for filename in os.listdir(r"src/cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with client:
        await load()
        await client.start(TOKEN)

asyncio.run(main())

# python src/index.py





