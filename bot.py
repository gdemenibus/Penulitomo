# bot.py
import asyncio
import json
import os
import random

import demoji
import discord
from dotenv import load_dotenv


def boot(coro):
    task = asyncio.create_task(coro)
    asyncio.get_running_loop().run_until_complete(task)
    return task.result()


class Penultimo(discord.Client):
    def __init__(self, guild, quotes):
        print("Penulitmo booting")
        intent = discord.Intents.default()
        intent.members = True
        super().__init__(intents=intent)
        self.jail = {"Inmate ID": 1}
        self.criminalRecord = {"Member ID": 1}
        self.guild = guild
        self.quotes: list = quotes
        # Function for getting voicelines

    def get_quote(self, keyword=None):
        if keyword is None:
            return random.choice(self.quotes)["phrase"]
        else:
            print("Functionality not made yet. Please pay more taxes")

    async def on_self_mention(self, message):
        await message.reply(self.get_quote())

    # Function to be called on mention
    async def check_mention(self, message):
        role_name = [x.name for x in message.role_mentions]
        if self.user in message.mentions or "Penultimo" in role_name:
            await self.on_self_mention(message)

    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")
        for guild in self.guilds:
            if guild.name == self.guild:
                break
        print(
            f"{self.user} is connected to the following guild: \n"
            f"{guild.name}(id: {guild.id})"
        )
        for guild in self.guilds:
            for role in guild.roles:
                if role.name == "Horny Rehab":
                    for member in role.members:
                        if member.id in self.jail:
                            continue
                        else:
                            self.jail[member.id] = 0

    def get_rehab_role(self, roles):
        for x in roles:
            if x.name == "Horny Rehab":
                return x

    async def place_in_jail(self, member, role):
        await member.add_roles(role)
        self.jail[member.id] = 0
        print(member.display_name + " was sent to jail")
        if member.id in self.criminalRecord:
            self.criminalRecord[member.id] += 1
        else:
            self.criminalRecord[member.id] = 1
        print("Jail now has: ")
        print(self.jail)

    async def custom_naughty(self, message):
        if ":plead:" in message.content:
            await message.channel.send(
                f"You know what you get "
                + message.author.mention
                + " for custom  emojis? Jail, right away, no trial, no nothing! "
            )
            print("Registered custom emoji sent by" + message.author.mention)
            rehab = self.get_rehab_role(message.guild.roles)
            await self.place_in_jail(message.author, rehab)

    async def emoji_check(self, message):
        emoji = demoji.findall(message.content)
        if message.guild is None:
            await message.channel.send(
                "Penultimo's loyalty is paramount. He does not take any bribes. If you want to bribe El Presidente, send your letters to @Gbus"
            )
            print("Message sent to penultimo on DM by" + message.author.mention)
            return
        if "pleading face" in emoji.values():
            await message.channel.send(
                message.author.mention + ", you're going straight to jail"
            )
            print("Emoji Registered sent by " + message.author.display_name)
            rehab = self.get_rehab_role(message.guild.roles)
            await self.place_in_jail(message.author, rehab)

    async def release_jail(self, author, message):
        rehab = self.get_rehab_role(message.guild.roles)
        await message.reply(
            "You've served your sentence. I hope I won't see you here again"
        )
        await author.remove_roles(rehab)

    # Message count relies on jail only containing people in jail.
    async def message_count(self, message):
        if message.guild is None:
            return
        author_id = message.author.id
        if author_id in self.jail:
            self.jail[author_id] += 1
            if self.jail[author_id] >= 25:
                self.jail.pop(author_id)
                await self.release_jail(message.author, message)

    async def jail_debug_print(self, message):
        if "jail debug" in message.content:
            print(self.jail)
            await message.reply(self.jail)  
    async def on_message(self, message):
        if message.author == self.user:
            return
        await self.jail_debug_print(message)
        await self.check_mention(message)
        await self.custom_naughty(message)
        await self.emoji_check(message)
        await self.message_count(message)

    async def on_reaction_add(self, reaction, user):
        if reaction.message.guild is None:
            await reaction.message.channel.send(
                "Penultimo is confused by your reaction. Are you trying to bribe Penultimo?"
            )
            return
        emoji = demoji.findall(str(reaction.emoji))
        if "pleading face" in emoji.values():
            rehab = self.get_rehab_role(reaction.message.guild.roles)
            await self.place_in_jail(user, rehab)
            await reaction.message.add_reaction(str("🚨"))
            print("Reaction logged by " + user.mention)


def main():
    load_dotenv()

    with open("quotes.json") as quotes:
        quotes_json = json.load(quotes)
    TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD = os.getenv("DISCORD_GUILD")
    if TOKEN is None:
        print("Token Missing")
        exit(1)
    penultimo = Penultimo(GUILD, quotes_json)
    penultimo.run(TOKEN)


if __name__ == "__main__":
    main()
