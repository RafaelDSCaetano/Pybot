from decouple import config
from discord.ext import commands
import os
bot = commands.Bot("*")

def load_cogs(bot):
    bot.load_extension("manager")
    #Carrega todos os arquivos da pasta Commands
    for file in os.listdir("Commands"):
        if file.endswith(".py"):
            cog = file[:-3]
            bot.load_extension(f"Commands.{cog}")
    #Carrega todos os arquivos da pasta Tasks
    for file in os.listdir("Tasks"):
        if file.endswith(".py"):
            cog = file[:-3]
            bot.load_extension(f"Tasks.{cog}")

load_cogs(bot)

TOKEN = config("TOKEN")
bot.run(TOKEN) 
