# bot.py
import os
import discord
import demoji
from dotenv import load_dotenv
load_dotenv()


TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
if TOKEN is None:
    print("Token Missing")
    exit(1)
client = discord.Client()


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f"{client.user} is connected to the following guild: \n"
        f"{guild.name}(id: {guild.id})"
    )


def get_rehab_role(roles):
    for x in roles:
        if x.name == "Horny Rehab":
            return x

@client.event
async def on_message(message):
    emoji = demoji.findall(message.content)
    if "pleading face" in emoji.values():
        print("Registered Horniness")
        await message.channel.send("JAIL")
        rehab = get_rehab_role(message.guild.roles)
        await message.author.add_roles(rehab)

@client.event
async def on_reaction_add(reaction,user):
    
    emoji = demoji.findall(str(reaction.emoji))
    if "pleading face" in emoji.values():
        rehab = get_rehab_role(reaction.message.guild.roles)
        await reaction.message.author.add_roles(rehab)
client.run(TOKEN)
