import discord
import requests
import os
import random
from dotenv import load_dotenv
load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print("Pronto a partire!")

@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.name == "general":
            general = channel
    if general and general.permissions_for(guild.me).send_messages:
        await general.send("Sono dentro")

@client.event
async def on_message(message):

    if message.content.upper().startswith("!HELP"):
        embed = discord.Embed(
            title = "Help", 
            description = "Ecco una lista di comandi che puoi usare con me:",
            colour = discord.Color.teal(),
            )
        embed.add_field(name="!help", value="Dovresti averlo capito :smirk:", inline=False)
        embed.add_field(name="!coronavirus", value="Fornisce i dati globali e italiani sul contagio del coronavirus", inline=False)
        embed.add_field(name="!ciao", value="Un piccolo gesto che mi rende felice :blush:", inline=False)
        embed.add_field(name="!lanciamoneta", value="Lancio una moneta, testa o croce?", inline=False)
        embed.add_field(name="!gif", value="Permettimi di cercare una Gif che possa cambiarti la giornata!", inline=False)
        await  message.channel.send(embed=embed)

    if message.content.upper().startswith("!CORONAVIRUS"):
        dati_totali = requests.get("https://coronavirus-tracker-api.herokuapp.com/all")
        dati_totali = dati_totali.json()
        totale_confermati = dati_totali["confirmed"]["latest"]
        totale_guariti = dati_totali["recovered"]["latest"]
        totale_decessi = dati_totali["deaths"]["latest"]
        confermati_italia = dati_totali["confirmed"]["locations"][16]["latest"]
        guariti_italia = dati_totali["recovered"]["locations"][16]["latest"]
        decessi_italia = dati_totali["deaths"]["locations"][16]["latest"]
        embed = discord.Embed(
            title = "Coronavirus", 
            description = "",
            colour = discord.Color.red(),
            )
        embed.add_field(name="Nel mondo", value=f"Totale casi confermati: {totale_confermati}\nGuariti: {totale_guariti}\nDecessi: {totale_decessi}", inline=False)
        embed.add_field(name="In Italia", value=f"Totale casi confermati: {confermati_italia}\nGuariti: {guariti_italia}\nDecessi: {decessi_italia}", inline=False)
        await message.channel.send(embed=embed)

    if message.content.upper().startswith("!CIAO"):
        await message.channel.send("Ciao :wave:")

    if message.content.upper().startswith("!LANCIAMONETA"):
        await message.channel.send(random.choice(["È uscito Testa", "È uscito Croce"]))

    if message.content.upper().startswith("!GIF"):
        chiave = os.getenv("GIPHYKEY")
        try:
            gif_tag = message.content[5:]
            if gif_tag == "":
                gif = requests.get(f"https://api.giphy.com/v1/gifs/random?api_key={chiave}&tag=&rating=G")
                gif = gif.json()
                gif = gif["data"]["image_url"]
                await  message.channel.send(f"Ecco a te una gif a caso presa da Giphy\n{gif}")
            else:
                gif = requests.get(f"https://api.giphy.com/v1/gifs/random?api_key={chiave}&tag={gif_tag}&rating=G")
                gif = gif.json()
                gif = gif["data"]["image_url"]
                await message.channel.send(f"Ecco a te una gif a caso con il tag {gif_tag} su Giphy\n{gif}")
        except TypeError:
            await message.channel.send("Sembra che questo tag non esista :thinking:")
        except AttributeError:
            await message.channel.send("Qualcosa non và :neutral_face:")
        except discord.errors.HTTPException:
            await message.channel.send("Non ho trovato nulla :poop:")

client.run(os.getenv("TOKEN"))