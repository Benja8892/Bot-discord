import openai
import discord
import tracemalloc
import asyncio

from discord.ext import commands
from discord import app_commands

openai.api_key = "sk-..."

class IA_bot(commands.Cog): 
    def __init__(self, client:commands.Bot):
       self.client = client



       
async def setup(client:commands.Bot) -> None:
  await client.add_cog(IA_bot(client))