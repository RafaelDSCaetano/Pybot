import discord
from discord.ext import commands, tasks
import datetime


class Dates(commands.Cog):
    """Work with dates"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.current_time.start()

    @tasks.loop(hours=1)
    async def current_time(self):

        now = datetime.datetime.now()

        HoursNow = int(now.strftime("%H"))

        now = now.strftime("%d/%m/%Y às %H:%M:%S")
        
        channel = self.bot.get_channel(902226910371807255)
       
        

        if 0 <= HoursNow and HoursNow < 6:
            print(HoursNow)
            await channel.send("Boa madrugada!\nData atual: " + now)
            
        elif 6 <= HoursNow and HoursNow < 12:
            print(HoursNow)
            await channel.send("Bom dia!\nData atual: " + now)
            
        elif 12 <= HoursNow and HoursNow < 18:
            print(HoursNow)
            await channel.send("Boa tarde!\nData atual: " + now)
            
        else:
            print(HoursNow)
            await channel.send("Boa noite!\nData atual: " + now)
            

def setup(bot):
    bot.add_cog(Dates(bot))