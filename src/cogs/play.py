
import discord
import tracemalloc
import re
import yt_dlp
import asyncio

from discord import app_commands
from discord import VoiceClient
from discord.utils import get
from discord import TextChannel

from enum import Enum
from urllib import parse, request
from discord.ext import commands
from discord import app_commands

class MusicPlayerState(Enum):
    STOPPED = 0  # When the player isn't playing anything
    PLAYING = 1  # The player is actively playing music.
    PAUSED = 2  # The player is paused on a song.
    WAITING = (
        3  # The player has finished its song but is still downloading the next one
    )
    DEAD = 4  # The player has been killed.

    def __str__(self):
        return self.name

class PlayerBotMusic(commands.Cog):
    def __init__(self, client:commands.Bot):
      self.client = client
      self.state = MusicPlayerState.STOPPED
      self.voice_client = None

    @commands.command()
    async def play(self, ctx, *, search):
      self.search = search

      YDL_OPTIONS = {'format': 'bestaudio/best',
                        'noplaylist': 'True',
                        'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'opus',
            }]}
      

      if not ctx.author.voice:
          await ctx.send("You are not connected to a voice channel.")


      """Obtenemos el chat de voz del autor que mando el mensaje y luego conectamos"""

      if self.state == MusicPlayerState.STOPPED:
        voice_channel = ctx.author.voice.channel
        self.voice_client = await voice_channel.connect()
        self.state = MusicPlayerState.PLAYING
      #Convierte search en una consulta lista para mandar a una URL para realizar una búsqueda en Youtube.
      query_string = parse.urlencode({'search_query': self.search})


      #en request pido todos los videos que se parezcan a querystring
      html_content = request.urlopen(f'http://www.youtube.com/results?search_query={query_string}')


      #En esta busco en el html recibido cual es el link de watch para enviarlo en el ctx.send
      search_results = re.findall(r'watch\?v=(\S{11})',html_content.read().decode())
      await ctx.send("https://www.youtube.com/watch?v=" + search_results[0])
      url = "https://www.youtube.com/watch?v=" + search_results[0]

      
      voice = get(self.client.voice_clients, guild=ctx.guild)
      with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
          info = ydl.extract_info(url, download=False)
          audio_url = info['url']
          source = await discord.FFmpegOpusAudio.from_probe(audio_url, method="fallback")
      self.voice_client.play(source=source)
      if voice.is_playing():
          ctx.send(await ctx.message.add_reaction('🎵')) # reaccion para confirmar que se está reproduciendo la canción
      else:
          ctx.send("ERROR") 


    @commands.command()
    async def join(self, ctx):
      if not ctx.author.voice:
          await ctx.send("You are not connected to a voice channel.")
      voice_channel = ctx.author.voice.channel
      
      if self.voice_client is None:
        self.voice_client = await voice_channel.connect()

      else:
         await self.voice_client.move_to(voice_channel)
      

    @commands.command()
    async def leave(self, ctx):
      if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel.")
      else:
        if self.voice_client:
          await self.voice_client.disconnect(force=True)


async def setup(client:commands.Bot) -> None:
  await client.add_cog(PlayerBotMusic(client))
