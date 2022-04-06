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
        return {'source': info['formats'][0]['url'], 'title': info['title'], 'thumbnail': info['thumbnail'], 'playlist': info['webpage_url']}


    def queue_list(self):
        description = ''
        for i in range(0, len(self.queue)):
            if i > 10: break
            description += f"{i+1}. {self.queue[i][0]['title']}\n"

        print(description)
        embed = discord.Embed(
            title=f"Musicas na queue",
            description = description,
            colour = 16744576
        )
        return embed





    def music_embed(self, ctx):
        playlist = self.queue[0][0]['playlist']
        thumbnail = self.queue[0][0]['thumbnail']
        title2 = self.queue[0][0]['title']
        embed = discord.Embed(
            title=f"{title2} | tocando!",
            description = playlist,
            colour = 16744576
        )
        embed.set_thumbnail(url = thumbnail)
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

        return embed

    def add_music_embed(self, ctx):
        playlist = self.queue[0][0]['playlist']
        thumbnail = self.queue[0][0]['thumbnail']
        title2 = self.queue[0][0]['title']
        embed = discord.Embed(
            title=f"{title2} | foi adicionado a queue!",
            description = playlist,
            colour = 16744576
        )
        embed.set_thumbnail(url = thumbnail)
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

        return embed

    def play_next(self, ctx):
        if len(self.queue) > 0:
            self.is_playing = True
            m_url = self.queue[0][0]['source']
            self.queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS))
            self.async_play(ctx)
            
        else:
            self.is_playing = False

    async def async_play(self, ctx):
        embed = self.music_embed(ctx)
        await ctx.send(embed = embed)
        self.play_next(ctx)
        


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
                
                embed = self.music_embed(ctx)
                await ctx.send(embed = embed)
                
                
                self.queue.pop(0)
                self.vc.play(discord.FFmpegPCMAudio(m_url,**self.FFMPEG_OPTIONS), after = lambda e: self.play_next(ctx))
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
                self.queue.append([song, voice_channel])
                embed = self.add_music_embed(ctx)          
                await ctx.send(embed = embed)

                if self.is_playing == False:
                    await self.play_music(ctx)

    @commands.command(aliases=["stop"])
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            await ctx.send("A música foi pausada")
        elif self.is_paused:
            self.vc.resume()
            await ctx.send("Música retomada")

    @commands.command(aliases=["r"])
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()
            embed = self.music_embed(ctx)
            await ctx.send(embed = embed)
        

    @commands.command(aliases=["s"])
    async def skip(self, ctx, *args):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.async_play(ctx)
    
    @commands.command(aliases=["q"])
    async def queue(self, ctx):
        
        if self.queue != []:
            embed = self.queue_list()
            await ctx.send(embed = embed)
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
        await ctx.send("Desconectado!") 


    @commands.command()
    async def tetra(self, ctx):
        voice_channel = ctx.author.voice.channel
        
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
        vc = ctx.voice_client
        ctx.voice_client.stop()
        vc.play(discord.FFmpegPCMAudio("e-tetra.mp3"))


    @commands.command()
    async def continued(self, ctx):
        voice_channel = ctx.author.voice.channel
        
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

        vc = ctx.voice_client
        ctx.voice_client.stop()
        vc.play(discord.FFmpegPCMAudio("to_be_continued.mp3"))
        
    


        
def setup(bot):
    bot.add_cog(Music(bot))