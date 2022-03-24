"""defines the Poll-Class which represents the Poll-object"""

import disnake
from disnake.channel import TextChannel
from disnake.message import Message
from asyncio import sleep
import datetime

class Poll(object):
    """Represents the Poll-Object which the Bot can create.

    Attributes
    -----------
    poll_name: :class:`str`
        The display-name of the poll.
    time: :class:`int`
        The lasting time of the poll.
    ans_number: :class:`int`
        The number of answers the poll consits of.
    answer_options: :class:`list`
        The list of answers.
    votes: :class:`list`
        The votes for each element of the answer_options list.
    mess: :class:`Message`
        The message, wich currently displays the poll in the TextChannel.
        Is ``None`` when there wasn't sent a message yet.
    emoji_list: :class:`list[str]`
        The default emoji list which stores the emojis representing
        the answer options of the poll.
    channel: :class:`TextChannel` or :class:`Thread`
        The Discord text-channel or Thread the poll belongs to.
    """

    def __init__(self, channel, ans_number = 0, time = 60, name = 'default'):
        self.poll_name: str = name
        self.time: int = time
        self.ans_number: int = 0
        self.answer_options: list = []
        self.votes: list = []
        self.mess = None
        self.emoji_list: list[str] = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        self.channel = channel

        for i in range(ans_number):
            self.new_ans_op("default_op " + str(i))

    async def new_ans_op(self, name: str):
        """adds a new answer option into the poll Object, adjusts ans_number and the votes list"""

        if self.ans_number == 11:
            await self.channel.send("Could not add '" +  name + "'. Maximum number of answer options reached.")
            return
        self.answer_options.append(name)
        self.ans_number += 1
        self.votes.append(0)

    async def del_ans_op(self, index: int):
        """deletes a answer option by list-index, adjusts ans_number and the votes list"""
        try:
            removed = self.answer_options.pop(index)
        except IndexError:
            self.channel.send("Answer could not be deleted (doesn't exist)")
         
        await self.channel.send("Removed '" + removed + "'")
        self.ans_number -= 1
        self.votes.pop(index)
        
    async def send_setup_Embed(self):
        """sends a new setup message (as Embed) in the Text-Channel and deletes the last setup Message,
        if this isn't the first one"""
        
        embed = disnake.Embed(title=self.poll_name, colour=disnake.Colour(0xc9a881),
                            description="\n**Current Settings:**\npoll name = '" +  self.poll_name +"'\ntime = "+ str(self.time) +" seconds\nnumber of answers = "+ str(self.ans_number) +"\n\n**Current answer oprions:**\n",
                            timestamp=datetime.datetime.now())

        for i in range(self.ans_number):
            embed.add_field(name=self.emoji_list[i], value=self.answer_options[i], inline=True)

        if self.mess != None:
            await self.mess.delete()
        self.mess = await self.channel.send(embed=embed)


    async def start(self):
        """starts the poll-Event"""

        await self.send_progress_Embed()
        await sleep(self.time)

    async def send_progress_Embed(self):
        """sends a new message (as Embed) which is shown while the poll is in progress, replaces and deletes current self.mess"""
        
        time = datetime.datetime.now() + datetime.timedelta(seconds=float(self.time))
        time = str(time)
        time = time.split(".")[0]
        embed = disnake.Embed(title=self.poll_name, colour=disnake.Colour(0xc9a881),
                            description = "Active Poll:\n\nReact with one of the given Emoji's to vote. The poll will end at "+ time +".\n\n**Answer Options are:**\n",
                            timestamp=datetime.datetime.now())

        for i in range(self.ans_number):
            embed.add_field(name=self.emoji_list[i], value=self.answer_options[i], inline=True)
        
        await self.mess.delete()
        self.mess = await self.channel.send(embed=embed)
        #await self.mess.pin()

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

        await self.send_result_Embed(winner)

    async def send_result_Embed(self, winner: int):
        """sends a new result-message (as Embed) which is shown after the poll-event ends also replaces and deletes the current self.mess, archives the Thread if 
        the poll is in a Thread"""
        
        embed = disnake.Embed(title=self.poll_name, colour=disnake.Colour(0xc9a881),
                            description= "**The Winner is drawn**\n\n" + self.answer_options[winner] + " has won the poll with " + str(self.votes[winner]-1) + " votes.",
                            timestamp=datetime.datetime.now())

        #await self.mess.unpin()
        await self.mess.delete()
        self.mess = await self.channel.send(embed=embed)
        if type(self.channel) is disnake.Thread:
            await self.channel.edit(archived=True)