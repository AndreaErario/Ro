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
            await client.send_message(message.channel, "Questo canale è già pronto per essere usato.\nSe hai bisogno di aiuto scrivi il comando !help per una lista di comandi")
        else:
            server = message.server
            await client.create_role(server, name="Bot Admin")
            await client.send_message(message.channel, "Un ruolo di nome Bot Admin è stato creato!\nSe sei il creatore del server devi assegnare quel ruolo a te stesso e a chi vuoi in modo che possiate usare i comandi del bot, assicurati però che il nuovo ruolo sia nel primo posto della lista dei ruoli\nScrivi il comando !help per una lista di comandi")
    
    
    if message.content.upper().startswith("!HELP"):
        await client.send_message(message.channel, "Ecco una lista dei comandi che puoi usare con me:\n\"!setup\": serve a preparare il server a essere utilizzato creando il ruolo \"Bot Admin\"\n\"!help\": Ormai dovresti saperlo :upside_down:\n\"!cookie\": :cookie:\n\"!say\": fai dire quello che vuoi al bot scrivendo la frase da fargli dire dopo il comando *\n\"!clear\": Cancella moltissimi messaggi dalla chat *\nI comandi affiancati da * possono essere usati solamente dalle persone che hanno il ruolo \"Bot Admin\" ")
    
    
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

    
    if message.content.upper().startswith("!CLEAR"):
        if "role" in [role.name for role in message.author.roles]:
            tmp = await client.send_message(message.channel, 'Cancellando...')
            async for msg in client.logs_from(message.channel):
                await client.delete_message(msg)
            await client.send_message(message.channel, 'Comando eseguito con successo! :wastebasket:')
        else:
            await client.send_message(message.channel, 'Scusa amico, non hai il permesso')
    
    
client.run(os.getenv("TOKEN"))
