"""defines the Poll-Class which represents the Poll-object"""

import discord
from discord.channel import TextChannel
from discord.message import Message
from asyncio import sleep
import datetime

class Poll(object):
    """Represents the Poll-Object which the Bot can create."""

    def __init__(self, ans_number, time = 60, name = 'default'):
        self.time = time
        self.ans_number = 0
        self.answer_options = []
        self.poll_name = name
        self.votes = []
        self.mess = None
        self.emoji_list = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        self.poll_status = 0 #zum abfragen mit welchem Emoji im Embed reagiert wurde 0-default 1-zeitänderung 2-namensänderung 3-13-Antwortmöglichkeitänderung

        for i in range(ans_number):
            self.new_ans_op("default_op " + str(i))

    def new_ans_op(self, name: str):
        """adds a new answer option into the poll Object, adjusts ans_number and the votes list"""

        self.answer_options.append(name)
        self.ans_number += 1
        self.votes.append(0)

    async def send_setup_Embed(self, channel: TextChannel):
        """sends a new setup message (as Embed) in the Text-Channel and deletes the last setup Message,
        if this isn't the first one"""
        
        embed = discord.Embed(title=self.poll_name, colour=discord.Colour(0xc9a881),
                            description="\n**This Message is to setup your poll:**\n\nCurrent Settings:\n\npoll name = '" +  self.poll_name +"'\ntime = "+ str(self.time) +" seconds\nnumber of answers = "+ str(self.ans_number) +"\n\n",
                            timestamp=datetime.datetime.utcnow())
        embed.add_field(name="0️⃣", value="React with the right number to rename your anwer options.", inline=True)
        embed.add_field(name="❌", value="React with this to delete your poll.", inline=True)
        embed.add_field(name="⏱", value="React with this to set the time of your poll.", inline=True)
        embed.add_field(name="✏", value="React with this to rename the poll.", inline=True)
        embed.add_field(name="✅", value="React with this to start the poll", inline=True)
        if self.mess != None:
            await self.mess.delete()
        self.mess = await channel.send(embed=embed)
        await self.mess.add_reaction("❌")
        await self.mess.add_reaction("⏱")
        await self.mess.add_reaction("✏")
        await self.mess.add_reaction("✅")
        for i in range(self.ans_number):
            await self.mess.add_reaction(self.emoji_list[i])

    async def start(self):
        """starts the poll-Event"""

        await self.send_progress_Embed(self.mess.channel)
        await sleep(self.time)

    async def send_progress_Embed(self, channel: TextChannel):
        """sends a new message (as Embed) which is shown while the poll is in progress, replaces and deletes current self.mess"""
        
        time = datetime.datetime.now() + datetime.timedelta(seconds=float(self.time))
        time = str(time)
        time = time.split(".")[0]
        embed = discord.Embed(title=self.poll_name, colour=discord.Colour(0xc9a881),
                            description = "Active Poll:\n\nReact with one of the given Emoji's to vote. The poll will end at "+ time +".\n\n**Answer Options are:**\n",
                            timestamp=datetime.datetime.utcnow())

        for i in range(self.ans_number):
            embed.add_field(name=self.emoji_list[i], value=self.answer_options[i], inline=True)
        
        await self.mess.delete()
        self.mess = await channel.send(embed=embed)
        await self.mess.pin()

        for i in range(self.ans_number):
            await self.mess.add_reaction(self.emoji_list[i])

    async def analyze_results(self, message: Message):
        """checks which answer has won the poll"""

        maxvotes = -1
        winner = -1

        for i in range(len(message.reactions)):
            for j in range(self.ans_number):
                if message.reactions[i].emoji == self.emoji_list[j]:
                    self.votes[j] = message.reactions[i].count
        
        for i in range(self.ans_number):
            if self.votes[i] > maxvotes:
                maxvotes = self.votes[i]
                winner = i

        await self.send_result_Embed(message.channel, winner)

    async def send_result_Embed(self, channel: TextChannel, winner: int):
        """sends a new result-message (as Embed) which is shown after the poll-event ends also replaces and deletes the current self.mess"""
        
        embed = discord.Embed(title=self.poll_name, colour=discord.Colour(0xc9a881),
                            description= "**The Winner is drawn**\n\n" + self.answer_options[winner] + " has won the poll with " + str(self.votes[winner]-1) + " votes.")

        await self.mess.unpin()
        await self.mess.delete()
        self.mess = await channel.send(embed=embed)