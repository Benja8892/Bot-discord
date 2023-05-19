from __future__ import unicode_literals
import os
from dotenv import load_dotenv

import discord
from discord import VoiceClient
from discord.utils import get
from discord.ext import commands
from discord import TextChannel

import yt_dlp
import asyncio
from urllib import parse, request
import re
import tracemalloc

#DISCORD BOT TOKEN
load_dotenv() 
discord_token = os.getenv("DISCORD_TOKEN")

tracemalloc.start()

intents = discord.Intents.all()
intents.members = True 
#PREFIJOS DE COMANDOS TIENE QUE EMPEZAR CON /
bot = commands.Bot(command_prefix="/", description='This is a helper bot',intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send("pong con sexto")

@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel.")

    voice_channel = ctx.author.voice.channel
    try:
        voice = await voice_channel.connect(reconnect=True)
    except NameError as errors:
        print(bot.voice_clients)
        if voice.is_connected():
            await voice.move_to(voice_channel)
            await ctx.send("jeje")


@bot.command()
async def play(ctx, *, search):
    if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel.")

    """Obtenemos el chat de voz del autor que mando el mensaje y luego conectamos"""
    voice_channel = ctx.author.voice.channel
    voice_client = await voice_channel.connect()

    #Convierte search en una consulta lista para mandar a una URL para realizar una búsqueda en Youtube.
    query_string = parse.urlencode({'search_query': search})

    #en request pido todos los videos que se parezcan a querystring
    html_content = request.urlopen(f'http://www.youtube.com/results?search_query={query_string}')

    #En esta busco en el html recibido cual es el link de watch para enviarlo en el ctx.send
    search_results = re.findall(r'watch\?v=(\S{11})',html_content.read().decode())
    await ctx.send("https://www.youtube.com/watch?v=" + search_results[0])
    url = "https://www.youtube.com/watch?v=" + search_results[0]

    YDL_OPTIONS = {'format': 'bestaudio/best',
                   'noplaylist': 'True',
                   'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'opus',
    }]}

    voice = get(bot.voice_clients, guild=ctx.guild)
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']
        source = await discord.FFmpegOpusAudio.from_probe(audio_url, method="fallback")
    voice_client.play(source=source)
    if voice.is_playing():
        ctx.send(await ctx.message.add_reaction('🎵')) # reaccion para confirmar que se está reproduciendo la canción
    else:
        ctx.send("ERROR") 


bot.run(discord_token)

# python src/index.py
