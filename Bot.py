#Creato da AndreaErario nel 2018

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get
import asyncio
import time
import os
import random
import safygiphy
import requests
import io


Client = discord.Client()
g = safygiphy.Giphy()
client = commands.Bot(command_prefix="!")

variabile = False

@client.event 
async def on_ready():
    print("Il Bot e' ora operativo")
    
@client.event
async def on_server_join(server):
    await client.send_message(server.owner, "Grazie per avermi aggiunto al tuo Server.\nSe vuoi sfruttarmi al meglio scrivi in un canale testuale del tuo Server il comando !setup che creerà il ruolo Bot Admin automaticamente.\nSe hai bisogno di una lista dei comandi puoi usare il comando !help")    

@client.event
async def on_message(message):
    
    if message.content.upper().startswith("!ALLSERVER"):
        if os.getenv("ID") in [message.author.id]:
            await client.send_message(message.channel, "Ecco la Lista dei Server a cui sono connesso:")
            for server in client.servers:
                await client.send_message(message.channel, "\nServer: {}\nProprietario: {}\n".format(server.name, server.owner))
        else:
            await client.send_message(message.channel, "Solo il mio padrone può usare questo comando")
    
    if message.content.upper().startswith("!SETUP"):
        if os.getenv("IDBOT") in [message.author.id]:
            await client.send_message(message.channel, "Perché mai dovrei usare un mio comando :thinking:")
        else:
            try:
                if "Bot Admin" in [role.name for role in message.server.roles]:
                    await client.send_message(message.channel, "Questo server è già pronto per essere usato.\nSe hai bisogno di aiuto scrivi il comando !help per una lista di comandi")
                else:
                    server = message.server
                    await client.create_role(server, name="Bot Admin")
                    await client.send_message(message.channel, "Un ruolo di nome Bot Admin è stato creato!\nSe sei il creatore del server devi assegnare il ruolo Bot Admin a te stesso e a chi vuoi in modo che possiate usare i comandi speciali del bot\nScrivi il comando !help per una lista di comandi")
            except AttributeError:
                await client.send_message(message.author, "Questo comando funziona solo nei Server")
    
    if message.content.upper().startswith("!HELP"):
        if os.getenv("IDBOT") in [message.author.id]:
            await client.send_message(message.channel, "Perché mai dovrei usare un mio comando :thinking:")
        else:
            embed = discord.Embed(
                title = "Help",
                description = "Ecco una lista di comandi che puoi usare con me:", 
                colour = discord.Color.teal()
            )
            embed.add_field(name="!setup", value="Serve a preparare il server a essere utilizzato creando il ruolo \"Bot Admin\"\n", inline=False)
            embed.add_field(name="!help", value="Ormai dovresti saperlo :upside_down:\n", inline=False)
            embed.add_field(name="!cookie", value=":cookie:\n", inline=False)
            embed.add_field(name="!lanciomoneta", value="Testa o Croce?", inline=False)
            embed.add_field(name="!gif", value="Manda una gif con il tag che ci scrivi di seguito o ne cerca una completamente a caso su Giphy (nel caso dovessi inserire un Tag inesistente verrà mostrato un messaggio d'errore)\n", inline=False)
            embed.add_field(name="!doveatterro", value="Se non sai dove lanciarti ti basterà usare questo comando che ti indicherà un posto casuale per atterrare", inline=False)
            embed.add_field(name="!reverse", value="Scrivi qualcosa dopo il comando per farlo scrivere al contrario", inline=False)
	   embed.add_field(name="!say *", value="Fai dire quello che vuoi al bot scrivendo la frase da fargli dire dopo il comando :speaking_head:\n", inline=False)
	    embed.add_field(name="!clear *", value="Cancella moltissimi messaggi dalla chat \n(ATTENZIONE non potrai più tornare indietro!)\n", inline=False)
	    embed.add_field(name="!superrole *", value="Cambia il colore di Bot Admin infinitamente, lo puoi fermare con il comando !stop (Ogni volta che il bot verrà aggiornato si fermerà :no_mouth:)", inline=False)
	    embed.add_field(name="!leave *", value="Elimina il ruolo \"Bot Admin\" e mi fa uscire dal Server\n", inline=False)
	    embed.add_field(name="Errori", value="Il Bot potrebbe mostrare un messaggio d'errore quando si usa nei messaggi diretti e quando qualcosa non và\n", inline=False)
            embed.set_footer(text="I comandi affiancati da * possono essere usati solamente dalle persone che hanno il ruolo \"Bot Admin\"")
            await client.send_message(message.channel, embed=embed)
            await client.send_message(message.channel, "Se hai bisogno di maggiori informazioni puoi visitare il sito \nhttps://andreaerario.pythonanywhere.com/Ro/Help")
    
    if message.content.upper().startswith('!COOKIE'):
        if os.getenv("IDBOT") in [message.author.id]:
            await client.send_message(message.channel, "Perché mai dovrei usare un mio comando :thinking:")
        else:
            try:
                await client.send_message(message.channel, ":cookie:")
            except discord.errors.NotFound:
                return
    
    if message.content.upper().startswith('!SAY'):
        if os.getenv("IDBOT") in [message.author.id]:
            await client.send_message(message.channel, "Perché mai dovrei usare un mio comando :thinking:")
        else:
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
                await client.send_message(message.author, "Questo comando funziona solo nei Server")
    
    if message.content.upper().startswith("!CLEAR"):
        if os.getenv("IDBOT") in [message.author.id]:
            await client.send_message(message.channel, "Perché mai dovrei usare un mio comando :thinking:")
        else:
            try:
                if "Bot Admin" in [role.name for role in message.author.roles] or os.getenv("ID") in [message.author.id]:
                    tmp = await client.send_message(message.channel, 'Cancellando...')
                    async for msg in client.logs_from(message.channel):
                        await client.delete_message(msg)
                    await client.send_message(message.channel, 'Comando eseguito con successo! :wastebasket:')
                else:
                    await client.send_message(message.channel, 'Scusa amico, non hai il permesso')
            except AttributeError:
                await client.send_message(message.author, "Questo comando funziona solo nei Server")
    
    
    if message.content.upper().startswith("!LANCIOMONETA"):
        if os.getenv("IDBOT") in [message.author.id]:
            await client.send_message(message.channel, "Perché mai dovrei usare un mio comando :thinking:")
        else:
            await client.send_message(message.channel, random.choice(["È uscito Testa", "È uscito Croce"]))
           
    
    if message.content.upper().startswith("!LEAVE"):
        if os.getenv("IDBOT") in [message.author.id]:
            await client.send_message(message.channel, "Perché mai dovrei usare un mio comando :thinking:")
        else:
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
                await client.send_message(message.channel, "Questo comando funziona solo nei Server")
    
    if message.content.upper().startswith("!GIF"):
        if os.getenv("IDBOT") in [message.author.id]:
            await client.send_message(message.channel, "Perché mai dovrei usare un mio comando :thinking:")
        else:
            try:
                gif_tag = message.content[5:]
                rgif = g.random(tag=str(gif_tag), rating="g")
                response = requests.get(
                    str(rgif.get("data", {}).get('image_original_url')), stream=True
                )
                if gif_tag == "":
                    await client.send_message(message.channel, "Sto cercando...")
                    await client.send_file(message.channel, io.BytesIO(response.raw.read()), filename='video.gif', content="Ho preso una gif a caso su Giphy")
                else:
                    await client.send_message(message.channel, "Sto cercando...")
                    await client.send_file(message.channel, io.BytesIO(response.raw.read()), filename='video.gif', content="Ho preso una gif a caso con il tag {} su Giphy".format(gif_tag))
            except AttributeError:
                await client.send_message(message.channel, "Qualcosa non và :neutral_face:")
            except discord.errors.HTTPException:
                await client.send_message(message.channel, "Non ho trovato nulla :poop:")

    if message.content.upper().startswith("!SUPERROLE"):
        if os.getenv("IDBOT") in [message.author.id]:
            await client.send_message(message.channel, "Perché mai dovrei usare un mio comando :thinking:")
        else:
            try:
                if "Bot Admin" in [role.name for role in message.author.roles] or os.getenv("ID") in [message.author.id]:
                    global variabile
                    if variabile == False:
                        variabile = True
                        await client.send_message(message.channel, "Il mio Potere scorre nel tuo nome :dragon:")
                    else:
                        await client.send_message(message.channel, "Il comando è gia attivo... assicurati di avere il ruolo Bot Admin")
                else:
                    await client.send_message(message.channel, "Scusa amico, non hai il permesso")
            except AttributeError:
                await client.send_message(message.channel, "Questo comando funziona solo nei Server")
    if message.content.upper().startswith("!SUPERROLE"):
        try:
            BotAdmin = discord.utils.get(message.server.roles, name="Bot Admin")      
            while variabile == True:
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.red())        
                time.sleep(0.1)
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.orange())
                time.sleep(0.1)
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.gold())
                time.sleep(0.1)
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.green())
                time.sleep(0.1)
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.blue())
                time.sleep(0.1)
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.purple())
                time.sleep(0.1)
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.teal())
                time.sleep(0.1)
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.red())        
                time.sleep(0.1)
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.orange())
                time.sleep(0.1)
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.gold())
                time.sleep(0.1)
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.green())
                time.sleep(0.1)
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.blue())
                time.sleep(0.1)
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.purple())
                time.sleep(0.1)
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.teal())
                time.sleep(0.1)
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.red())        
                time.sleep(0.1)
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.orange())
                time.sleep(0.1)
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.gold())
                time.sleep(0.1)
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.green())
                time.sleep(0.1)
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.blue())
                time.sleep(0.1)
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.purple())
                time.sleep(0.1)
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.teal())
                time.sleep(0.1)
                await client.edit_role(message.server, BotAdmin, colour = discord.Color.default())
                time.sleep(0.1)
        except AttributeError:
            None
    if message.content.upper().startswith("!STOP"):
        if os.getenv("IDBOT") in [message.author.id]:
            await client.send_message(message.channel, "Perché mai dovrei usare un mio comando :thinking:")
        else:
            try:
                if "Bot Admin" in [role.name for role in message.author.roles] or os.getenv("ID") in [message.author.id]:
                    if variabile == False:
                        await client.send_message(message.channel, "Non puoi fermare un comando non ancora funzionante :upside_down:")
                    else:
                        variabile = False
                        await client.send_message(message.channel, "Il mio Potere è stato fermato")
                else:
                    await client.send_message(message.channel, "Scusa amico, non hai il permesso")
            except AttributeError:
                await client.send_message(message.channel, "Questo comando funziona solo nei Server")
    
    if message.content.upper().startswith("!DOVEATTERRO"):
        if os.getenv("IDBOT") in [message.author.id]:
            await client.send_message(message.channel, "Perché mai dovrei usare un mio comando :thinking:")
        else:
            await client.send_message(message.channel, random.choice(["Crocevia del Ciarpame","Passatempi Pomposi","Rapide Rischiose","Bosco Blaterante","Tempio Tomato","Sponde del Saccheggio","Parco Pacifico","Montagnole Maledette","Spiagge Snob","Pinnacoli Pendenti","Sprofondo Stantio","Corso Commercio","Rifugio Ritirato","Borgo Bislacco","Condotti Confusi","Boschetto Bisunto","Laboratorio della Latrina","Approdo Avventurato","Lande Letali","Palmeto Paradisiaco"]))   
     
    if message.content.upper().startswith("!REVERSE"):
	if os.getenv("IDBOT") in [message.author.id]:
            await client.send_message(message.channel, "Perché mai dovrei usare un mio comando :thinking:")
        else:
	    stringa = message.content[9:]
            if stringa == "":
                await client.send_message(message.channel, "Inserisci qualcosa dopo il comando")
            else:
                indice = (len(stringa) -1)
                nuovastringa = ""
                while indice >= 0:
	            nuovastringa += stringa[indice]
	            indice -= 1
                await client.send_message(message.channel, "{}".format(nuovastringa))
    
client.run(os.getenv("TOKEN"))
