import datetime
import discord
from discord import client
from discord.message import Message
import wikipedia
from asyncio import sleep


class MyClient(discord.Client):
    r"""Represents the Bot-Client"""

    def __init__(self):
        discord.Client.__init__(self)
        self.poll_list = []
        self.wiki_default_lang = "de"
        self.help_text = "!wiki (?[Sprachkürzel]) [Suchbegriff] --> Wikipediazusammenfassung des Suchbegriffes in gewünschter Sprache (standardmäßig deutsch)"
        self.emoji_list = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]

    #bot ist eingeloggt
    async def on_ready(self):
        print("Bot is online")
        await client.change_presence(activity=discord.Game("!help"), status=discord.Status.online)
    
    #nachricht wird in channel gepostet
    async def on_message(self, message: Message):
        if message.author == client.user:
            return
        elif message.content.startswith("!wiki "):
            await wiki(message)
        elif message.content.startswith("!poll "):
            await poll_func(message)
        elif message.content == "!help":
            await message.channel.send(client.help_text)

class poll(object):
    r"""Represents the poll-Object which the Bot can create."""

    def __init__(self, time = 60, name = 'default'):
        self.time = time
        self.ans_number = 0
        self.answer_options = []
        self.poll_name = name
        self.votes = []

    def new_ans_op(self, name: str):
        self.answer_options.append(name)
        self.ans_number += 1
        self.votes.append(0)


#Realisierung der Wiki-Funktion (es funktioniert irgendwie nicht wenn ich diese Funktion mit in die MyClient-Klasse mache)
async def wiki(message: Message):
    val = message.content.split(" ", 1)[1]

    #Sprachparameter auswerten
    if val.startswith("?"):
        searchval = val.split(" ", 1)[1]
        param = val.split(" ", 1)[0].replace("?", "")
        if param in wikipedia.languages():
            wikipedia.set_lang(param)
        else:
            await message.channel.send('Language "' + param + '" is not supported')
            return
    else:
        searchval = val
    try:
        title = wikipedia.search(searchval)[0]
        page = wikipedia.page(title=title, auto_suggest=False)
        #Embed descriptions have a character Limit of 4096
        string = page.summary
        string = string + "\n[original Artikel](" + page.url + ")"
        
        i = 10
        while len(string) > 4096:
            string = wikipedia.summary(title=title, sentences=i) + "\n[original Artikel](" + page.url + ")"
            i -= 1
        embed = discord.Embed(title = page.title, description = string, color = 0xcacfc9, timestamp=datetime.datetime.utcnow())
        pictures = page.images
        if len(pictures) > 0:
            embed.set_thumbnail(url=pictures[0])

        await message.channel.send(embed=embed)

    except Exception as e:
        await message.channel.send(str(e))
    wikipedia.set_lang(client.wiki_default_lang) 
    return

#Realisierung der Poll Funktion des Bots
async def poll_func(message: Message):
    val = message.content.split(" ", 1)[1]
    param = val.split(" ", 1)

    if param[0] == "create":
        client.poll_list.append(poll(name=param[1]))
        await message.channel.send("poll " + param[1] + " created")
    elif param[0] == "st":
        client.poll_list[0].time = int(param[1])
        await message.channel.send("set time of poll to " + param[1] + " seconds")
    elif param[0] == "ao":
        client.poll_list[0].new_ans_op(param[1])
        await message.channel.send("added vote option " + param[1])
    elif param[0] == "start":
        temp_number = 0
        string = ""

        for i in client.poll_list[0].answer_options:
            string = string + "\n" + str(temp_number) + " " + i
            temp_number += 1
        send_msg = await message.channel.send(string)
        temp_number = client.poll_list[0].ans_number

        for i in client.emoji_list:
            await send_msg.add_reaction(i)
            temp_number -= 1
            if temp_number == 0: break
        await sleep(client.poll_list[0].time)
        temp_number = 0
        index = -1
        send_msg = discord.utils.get(client.cached_messages, id=send_msg.id)

        for i in range(len(send_msg.reactions)):
            if send_msg.reactions[i].count > temp_number:
                temp_number = send_msg.reactions[i].count
                index = i
        await message.channel.send("Abstimmung wurde beendet\n '" + client.poll_list[0].answer_options[index] + "' hat die Abstimmung mit " + str(temp_number -1) + " votes gewonnen!")
        del client.poll_list[0]

client = MyClient()
wikipedia.set_lang(client.wiki_default_lang) #Sprache ändern
client.run("ODc5NzM4MzM0NzU3Mzg4Mzc4.YSUGKw.I0t9FBgfEvcPtcEVyoe5KbGF2-s")