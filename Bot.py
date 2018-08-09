#Creato da AndreaErario nel 2018

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
    
    if message.content.upper().startswith("!SETUP"):
        if "Bot Admin" in [role.name for role in message.server.roles]:
            await client.send_message(message.channel, "Questo canale è già pronto per essere usato")
        else:
            server = message.server
            await client.create_role(server, name="Bot Admin")
            await client.send_message(message.channel, "Un ruolo di nome Bot Admin è stato creato se sei il padrone del server devi aggiungere quel ruolo a chi vuoi assicurandoti che sia nel primo posto della lista e che abbia i permessi di amministratore")
    
    
    if message.content.upper().startswith('!COOKIE'):
        try:
            await client.delete_message(message)
            await client.send_message(message.channel, ":cookie:")
        except discord.errors.NotFound:
            return
    
    
    if message.content.upper().startswith('!SAY'):
        if "Bot Admin" in [role.name for role in message.author.roles]:
            args = message.content.split(" ")
            try:
                await client.delete_message(message)
                await client.send_message(message.channel,"%s " % (" ".join(args[1:])))
            except discord.errors.NotFound:
                return
        else:
            await client.send_message(message.channel, "Scusa amico, non hai il permesso")


client.run(os.getenv("TOKEN"))
