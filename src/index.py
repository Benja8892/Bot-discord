import os
from dotenv import load_dotenv

import discord
from discord import FFmpegPCMAudio, VoiceClient
from discord.utils import get
from discord.ext import commands
from discord import TextChannel

from youtube_dl import YoutubeDL
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
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to()
    else:
        await voice.connect(reconnect=True)

async def download_video_to_pass(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
    'options': '-vn'
    }
    voice = get(bot.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.message.add_reaction('🎵') # reaccion para confirmar que se está reproduciendo la canción
        # while voice.is_playing():
        #     await asyncio.sleep(1)
        # await voice.disconnect()
        # reproducir el audio en Discord
        # if voice and voice.is_connected():
        #     await voice.move_to()
        # else:
        #     voice = await ctx.author.voice.channel.connect()
            # voice.play(discord.FFmpegPCMAudio(executable='ffmpeg'))

            # espera a que termine de reproducirse el audio antes de desconectar el bot



@bot.command()
async def play(ctx, *, search):
    #Convierte search en una consulta lista para mandar a una URL para realizar una búsqueda en Youtube.
    query_string = parse.urlencode({'search_query': search})

    #en request pido todos los videos que se parezcan a querystring
    html_content = request.urlopen(f'http://www.youtube.com/results?search_query={query_string}')

    #En esta busco en el html recibido cual es el link de watch para enviarlo en el ctx.send
    search_results = re.findall(r'watch\?v=(\S{11})',html_content.read().decode())
    await ctx.send("https://www.youtube.com/watch?v=" + search_results[0])
    url = "https://www.youtube.com/watch?v=" + search_results[0]
    download_video_to_pass(url=url)

bot.run(discord_token)

# python src/index.py