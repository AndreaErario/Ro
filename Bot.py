#Creato da AndreaErario nel 2018

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get
import asyncio
import time
import os
import random


Client = discord.Client()  
client = commands.Bot(command_prefix="!")


@client.event 
async def on_ready():
    print("Il Bot e' ora operativo")

@client.event
async def on_message(message):
    
    if message.content.upper().startswith("!SETUP"):
        try:
            if "Bot Admin" in [role.name for role in message.server.roles]:
                await client.send_message(message.channel, "Questo server è già pronto per essere usato.\nSe hai bisogno di aiuto scrivi il comando !help per una lista di comandi")
            else:
                server = message.server
                await client.create_role(server, name="Bot Admin")
                await client.send_message(message.channel, "Un ruolo di nome Bot Admin è stato creato!\nSe sei il creatore del server devi assegnare quel ruolo a te stesso e a chi vuoi in modo che possiate usare i comandi speciali del bot\nScrivi il comando !help per una lista di comandi")
        except AttributeError:
            await client.send_message(message.author, "Questo comando funziona solo nei server")
    
    if message.content.upper().startswith("!HELP"):
        embed = discord.Embed(
            title = "Help",
            description = "Ecco una lista di comandi che puoi usare con me:", 
            colour = discord.Color.dark_blue()
        )
        embed.add_field(name="!setup", value="Serve a preparare il server a essere utilizzato creando il ruolo \"Bot Admin\"\n", inline=False)
        embed.add_field(name="!help", value="Ormai dovresti saperlo :upside_down:\n", inline=False)
        embed.add_field(name="!cookie", value=":cookie:\n", inline=False)
        embed.add_field(name="!lanciomoneta", value="Testa o Croce?", inline=False)
        embed.add_field(name="!say *", value="Fai dire quello che vuoi al bot scrivendo la frase da fargli dire dopo il comando :speaking_head:\n", inline=False)
        embed.add_field(name="!clear *", value="Cancella moltissimi messaggi dalla chat \n(ATTENZIONE non potrai più tornare indietro!)\n", inline=False)
        embed.add_field(name="!leave *", value="Elimina il ruolo \"Bot Admin\" e mi fa uscire dal Server\n", inline=False)
        embed.set_footer(text="I comandi affiancati da * possono essere usati solamente dalle persone che hanno il ruolo \"Bot Admin\"")
        await client.send_message(message.channel, embed=embed)
        await client.send_message(message.channel, "Se hai bisogno di maggiori informazioni puoi visitare il sito \nhttp://andreaerario.pythonanywhere.com/BotDiscord/Help")
    
    
    if message.content.upper().startswith('!COOKIE'):
        try:
            await client.send_message(message.channel, ":cookie:")
        except discord.errors.NotFound:
            return
    
    
    if message.content.upper().startswith('!SAY'):
        try:
            if "Bot Admin" in [role.name for role in message.author.roles] or os.getenv("ID") in [message.author.id]:
                args = message.content.split(" ")
                try:
                    await client.delete_message(message)
                    await client.send_message(message.channel,"%s " % (" ".join(args[1:])))
                except discord.errors.NotFound:
                    return
            else:
                await client.send_message(message.channel, "Scusa amico, non hai il permesso")
        except AttributeError:
            await client.send_message(message.author, "Questo comando funziona solo nei server")
    
    if message.content.upper().startswith("!CLEAR"):
        try:
            if "Bot Admin" in [role.name for role in message.author.roles] or os.getenv("ID") in [message.author.id]:
                tmp = await client.send_message(message.channel, 'Cancellando...')
                async for msg in client.logs_from(message.channel):
                    await client.delete_message(msg)
                await client.send_message(message.channel, 'Comando eseguito con successo! :wastebasket:')
            else:
                await client.send_message(message.channel, 'Scusa amico, non hai il permesso')
        except AttributeError:
            await client.send_message(message.author, "Questo comando funziona solo nei server")
    
    
    if message.content.upper().startswith("!LANCIOMONETA"):
        await client.send_message(message.channel, random.choice(["È uscito Testa", "È uscito Croce"]))
    
    
    if message.content.upper().startswith("!LEAVE"):
        try:
            if "Bot Admin" in [role.name for role in message.author.roles] or os.getenv("ID") in [message.author.id]:
                if "Bot Admin" in [role.name for role in message.server.roles]:
                    role = get(message.server.roles, name = "Bot Admin")
                    await client.delete_role(message.server, role)
                    await client.send_message(message.channel, "Il ruolo Bot Admin è stato eliminato")
                    await client.send_message(message.channel, "Sono uscito dal Server")
                    await client.leave_server(message.server)
                else:
                    await client.send_message(message.channel, "Sono uscito dal Server")
                    await client.leave_server(message.server)
            else:
                await client.send_message(message.channel, 'Scusa amico, non hai il permesso')
        except AttributeError:
            await client.send_message(message.channel, "Qualcosa non và :neutral_face:")
            
        
        
    
client.run(os.getenv("TOKEN"))
