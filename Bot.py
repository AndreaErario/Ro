import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import os


Client = discord.Client()  
client = commands.Bot(command_prefix="!")


@client.event 
async def on_ready():
    print("Il Bot e' ora operativo")

@client.event
async def on_message(message):
    
    if message.content.upper().startswith('!COOKIE'):
        try:
            await client.delete_message(message)
            await client.send_message(message.channel, ":cookie:")
        except discord.errors.NotFound:
            return
    
    
    if message.content.upper().startswith('!SAY'):
        if "role" in [role.name for role in message.author.roles]:
            args = message.content.split(" ")
            try:
                await client.delete_message(message)
                await client.send_message(message.channel,"%s " % (" ".join(args[1:])))
            except discord.errors.NotFound:
                return
        else:
            await client.send_message(message.channel, "Scusa amico, non hai il permesso")


client.run(os.getenv"TOKEN")
