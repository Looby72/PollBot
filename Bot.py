import datetime
import discord
from discord import client
from discord.message import Message
from discord.reaction import Reaction
from discord.user import User
from asyncio import sleep
import wiki

class MyClient(discord.Client):
    """Represents the Bot-Client"""

    def __init__(self):
        discord.Client.__init__(self)
        self.poll_list = []
        self.poll_status = 0 #zum abfragen mit welchem Emoji im Embed reagiert wurde 0-default 1-zeitänderung 2-namensänderung 3-13-Antwortmöglichkeitänderung
        self.help_text = "!wiki (?[Sprachkürzel]) [Suchbegriff] --> Wikipediazusammenfassung des Suchbegriffes in gewünschter Sprache (standardmäßig deutsch)"
        self.emoji_list = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]

    
    async def on_ready(self):
        """Called when the Bot Client is logged in after the start."""

        print("Bot is online")
        await client.change_presence(activity=discord.Game("!help"), status=discord.Status.online)
    
    async def on_message(self, message: Message):
        """Called when a message is posted in a channel which the bot can read."""

        if message.author == client.user:
            return
        elif message.content.startswith("!wiki "):
            await wiki.wiki_main(message)
        elif message.content.startswith("!poll "):
            await poll_func1(message)
        elif message.content == "!help":
            await message.channel.send(client.help_text)
        elif self.poll_status != 0 and message.channel == self.poll_list[0].mess.channel:
            if self.poll_status == 1:
                self.poll_list[0].time = int(message.content)

            elif self.poll_status == 2:
                self.poll_list[0].poll_name = message.content
                
            elif self.poll_status == 3:
                self.poll_list[0].answer_options[0] = message.content
                
            elif self.poll_status == 4:
                self.poll_list[0].answer_options[1] = message.content
                
            elif self.poll_status == 5:
                self.poll_list[0].answer_options[2] = message.content
                
            elif self.poll_status == 6:
                self.poll_list[0].answer_options[3] = message.content
                
            elif self.poll_status == 7:
                self.poll_list[0].answer_options[4] = message.content
                
            elif self.poll_status == 8:
                self.poll_list[0].answer_options[5] = message.content
                
            elif self.poll_status == 9:
                self.poll_list[0].answer_options[6] = message.content
                
            elif self.poll_status == 10:
                self.poll_list[0].answer_options[7] = message.content
                
            elif self.poll_status == 11:
                self.poll_list[0].answer_options[8] = message.content
                
            elif self.poll_status == 12:
                self.poll_list[0].answer_options[9] = message.content
                
            elif self.poll_status == 13:
                self.poll_list[0].answer_options[10] = message.content
            self.poll_status == 0
            await self.poll_list[0].send_Embed(message.channel)    
            
    #reaction added on a message (not called when message not in internal message-cache)
    async def on_reaction_add(self, reaction: Reaction, user: User):
        """Called when a reaction has been added to a message in a channel which the bot can read.
        (not called when message is not in internal message-chache of the Bot)"""

        if user == client.user:
            return
        if reaction.message.id == self.poll_list[0].mess.id:
            if reaction.emoji == "❌":
                del self.poll_list[0]
                await reaction.message.channel.send("Vote deleted")
                
            elif reaction.emoji == "⏱":
                self.poll_status = 1
                
            elif reaction.emoji == "✏":
                self.poll_status = 2
                
            elif reaction.emoji == "✅":
                await self.poll_list[0].start()
                
            for i in range(len(self.emoji_list)):
                if reaction.emoji == self.emoji_list[i]:
                    self.poll_status = i+3
                    
        

class poll(object):
    """Represents the poll-Object which the Bot can create."""

    def __init__(self, ans_number, time = 60, name = 'default'):
        self.time = time
        self.ans_number = 0
        self.answer_options = []
        self.poll_name = name
        self.votes = []
        self.mess = None

        for i in range(ans_number):
            self.new_ans_op("default_op " + str(i))

    def new_ans_op(self, name: str):
        self.answer_options.append(name)
        self.ans_number += 1
        self.votes.append(0)

    async def send_Embed(self, channel):
        embed = discord.Embed(title=self.poll_name, colour=discord.Colour(0xc9a881), description="\n**This Message is to setup your poll:**\n\nCurrent Settings:\n\npoll name = '" +  self.poll_name +"'\ntime = "+ str(self.time) +" seconds\nnumber of answers = "+ str(self.ans_number) +"\n\n", timestamp=datetime.datetime.utcnow())
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
            await self.mess.add_reaction(client.emoji_list[i])

    async def start(self):
        temp_number = 0
        string = ""

        for i in self.answer_options:
            string = string + "\n" + str(temp_number) + " " + i
            temp_number += 1
        send_msg = await self.mess.channel.send(string)

        temp_number = self.ans_number
        for i in client.emoji_list:
            await send_msg.add_reaction(i)
            temp_number -= 1
            if temp_number == 0: break
        await sleep(self.time)

        temp_number = 0
        index = -1
        send_msg = discord.utils.get(client.cached_messages, id=send_msg.id)

        for i in range(len(send_msg.reactions)):
            if send_msg.reactions[i].count > temp_number:
                temp_number = send_msg.reactions[i].count
                index = i
        await send_msg.channel.send("Abstimmung wurde beendet\n '" + client.poll_list[0].answer_options[index] + "' hat die Abstimmung mit " + str(temp_number -1) + " votes gewonnen!")
        del client.poll_list[0]


#to create a new poll
async def poll_func1(message: Message):
    """Calls the poll-constructor and stores the poll-object in MyClient.poll_list.
    Starts the 'poll sequence'."""

    value = int(message.content.split(" ", 1)[1])
    client.poll_list.append(poll(value))
    await client.poll_list[0].send_Embed(message.channel)

client = MyClient()
#wikipedia.set_lang(client.wiki_default_lang) #Sprache ändern
client.run("ODc5NzM4MzM0NzU3Mzg4Mzc4.YSUGKw.I0t9FBgfEvcPtcEVyoe5KbGF2-s")