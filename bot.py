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
intent = discord.Intents.default()
intent.members = True
client = discord.Client(intents = intent)

message_amount = 0

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
    global message_amount
    message_amount = message_amount + 1 
    emoji = demoji.findall(message.content)
    if "pleading face" in emoji.values():
        print("Registered Horniness")
        await message.channel.send(message.author.mention + ", you're going straight to jail" )
        rehab = get_rehab_role(message.guild.roles)
        await message.author.add_roles(rehab)
    if message_amount == 100:
        guild = client.get_guild(message.guild.id)
        message_amount = 0
        for x in guild.roles:
            if x.name == "Horny Rehab":
                for member in x.members:
                    await member.remove_roles(x)

@client.event
async def on_reaction_add(reaction,user):
    
    emoji = demoji.findall(str(reaction.emoji))
    if "pleading face" in emoji.values():
        rehab = get_rehab_role(reaction.message.guild.roles)
        await user.add_roles(rehab)
client.run(TOKEN)
