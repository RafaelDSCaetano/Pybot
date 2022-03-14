import discord
from discord.ext import commands
from youtube_dl import YoutubeDL





class Music(commands.Cog):
    """Work with music"""

    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.is_paused =False
        self.queue = []
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.YDL_OPTIONS = {'format': "bestaudio"}
        self.vc = None

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.queue) > 0:
            self.is_playing = True

            m_url = self.queue[0][0]['source']

            self.queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if len(self.queue)>0:
            self.is_playing = True
            m_url = self.queue[0][0]['source']

            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.queue[0][1].connect()

                if self.vc == None:
                    await ctx.send("Não foi possível conectar no canal de voz")
                    return
                else:
                    await self.vc.move_to(self.queue[0][1])

                self.queue.pop(0)
                self.vc.play(discord.FFmpegPCMAudio(m_url,**self.FFMPEG_OPTIONS), after=lambda e: self.play_next())

            else:
                self.is_playing = False

    @commands.command(aliases=["p", "playing"])
    async def play (self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("PyBot está conectado!")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Não foi possível adicionar sua musica.")
            else:
                await ctx.send("Musica adicionada a queue!")
                self.queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music(ctx)

    @commands.command(aliases=["stop"])
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.vc.resume()

    @commands.command(aliases=["r"])
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command(aliases=["s"])
    async def skip(self, ctx, *args):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)
    
    @commands.command(aliases=["q"])
    async def queue(self, ctx):
        retval = ""

        for i in range(0, len(self.queue)):
            if i > 4: break
            retval+= self.queue[i][0]['title'] + '\n'

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("Não tem musicas na queue")

    @commands.command()
    async def clear(self, ctx, *args):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Queue foi limpa!")

    @commands.command(name="leave", aliases=['disconnect', "l", "d", "quit"])
    async def leave(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()







    # @commands.command(aliases=["disconnect"])
    # async def quit(self, ctx):
    #     await ctx.voice.quit()

    # @commands.command(aliases=["q", "queue"])
    # async def queue(self, ctx, url):
    #     self.queue.append(url)
    #     await ctx.send("Uma musica foi adicionada a queue!")
    #     print(self.queue)
        

    # @commands.command(aliases=["p", "play"])
    # async def play(self, ctx, url):
    #     if ctx.author.voice is None:
    #         await ctx.send("Você não está em um canal de voz")
    #     voice_channel = ctx.author.voice.channel
    #     if ctx.voice_client is None:
    #         await voice_channel.connect()
    #     else:
    #         await ctx.voice_client.move_to(voice_channel)
    #     if self.queue != []:
    #         self.queue.append(url)
    #         await ctx.send("Uma musica foi adicionada a queue!")
    #     else:
    #         self.queue.append(url)
            
    #         vc = ctx.voice_client
    #         with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
    #             info = ydl.extract_info(url, download=False)
    #             url = str(self.queue[0])
    #             url2 = info['formats'][0]['url']
    #             source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
    #             vc.play(source)
    #             self.queue.pop(0)
                

    # @commands.command()
    # async def tetra(self, ctx):
    #     voice_channel = ctx.author.voice.channel
        
    #     if ctx.voice_client is None:
    #         await voice_channel.connect()
    #     else:
    #         await ctx.voice_client.move_to(voice_channel)
    #     vc = ctx.voice_client
    #     ctx.voice_client.stop()
    #     vc.play(discord.FFmpegPCMAudio("e-tetra.mp3"))


    # @commands.command()
    # async def continued(self, ctx):
    #     voice_channel = ctx.author.voice.channel
        
    #     if ctx.voice_client is None:
    #         await voice_channel.connect()
    #     else:
    #         await ctx.voice_client.move_to(voice_channel)

    #     vc = ctx.voice_client
    #     ctx.voice_client.stop()
    #     vc.play(discord.FFmpegPCMAudio("to_be_continued.mp3"))


    # @commands.command()
    # async def pause(self,ctx):
    #     await ctx.voice_client.pause()
    #     await ctx.send("Pausado!")


    # @commands.command()
    # async def resume(self,ctx):
    #     await ctx.voice_client.resume()
    #     await ctx.send("REEEEETOMADO!")


    # @commands.command()
    # async def stop(self,ctx):
    #     await ctx.voice_client.stop()
    #     await ctx.send("Stop!")
        
            


def setup(bot):
    bot.add_cog(Music(bot))