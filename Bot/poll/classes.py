#disnake imports
import disnake
from disnake.channel import TextChannel, Thread
from disnake.message import Message
from disnake import Embed, Colour
#asyncio imports
from asyncio import sleep
#datetime imports
from datetime import datetime, timedelta

class AnswerOption(object):
    """Represents an answer option in an Poll Object.
    
    Attributes
    -----------
    name: :class:`str`
        The String representing the answer option.
    votes: :class:`int`
        Number of votes on this Option."""

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.votes: int = 0

    def __str__(self) -> str:
        return self.name


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
    answer_options: :class:`list[AnswerOption]`
        The list of all answer options of the poll.
    mess: :class:`Message`
        The message, wich currently displays the poll in the TextChannel.
        Is ``None`` when there wasn't sent a message yet.
    emojis: :class:`list[str]`
        The default emoji list which stores the emojis representing
        the answer options of the poll.
    channel: :class:`TextChannel | Thread`
        The Discord text-channel or Thread the poll belongs to.
    """

    def __init__(self, channel: TextChannel | Thread, ans_number: int = 0, time: int  = 60, name: str = 'default'):
        """Poll Constructor sets:
        poll_name, time, ans_number, emojis (same in evry Poll object), channel

        Note:
        ans_number should be between 0 and 11, otherwise the function will fail with
        `PollException`

        calls the Poll.add_answer ans_number times with name = default_option {number}"""

        self.poll_name: str = name
        self.time: int = time
        self.ans_number: int = 0
        self.answer_options: list[AnswerOption] = []
        self.mess: Message = None
        self.emojis: list[str] = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        self.channel: TextChannel | Thread = channel

        if ans_number > 11:
            raise PollError("Maximum of 11 answers per Poll are allowed")

        if ans_number < 0:
            raise PollError(f"ans_number must be positive! (ans_number was {ans_number})")

        for i in range(ans_number):
            self.add_answer(name= f"default_option {i}")

    def add_answer(self, name: str):
        """Adds a new `AnswerOption` into the answer_options list.
        Raises PollError if name has > 30 Characters or if ans_number is == 11."""

        if self.ans_number == 11:
            raise PollError(f"Could not add answer '{name}'. Maximum number of answer options reached.")

        if len(name) > 30:
            raise PollError(f"Could not add answer '{name}'. Maximum of 30 Charactes are allowed.")

        self.answer_options.append(AnswerOption(name))
        self.ans_number += 1

    def delete_answer(self, index: int) -> AnswerOption:
        """Deletes an answer option by list-index
        returns the deleted answer Option"""

        try:
            removed = self.answer_options.pop(index)
        except IndexError:
            raise PollError("Answer could not be deleted (doesn't exist)")
         
        self.ans_number -= 1
        return removed

    def __str__(self) -> str:
        #TODO implement this to get all information of the object
        pass

    async def start(self):
        """Calls the entry function of PollSchedule to start the poll event"""

        if self.ans_number < 2:
            raise PollError("Cannot start poll with less than 2 answer options.")
        
        await PollSchedule.start(self)


class PollError(Exception):
    """Custom Exception-Class for all Exceptions raised in the Poll-Class"""

    def __init__(self, error: str) -> None:
        self.error_message = error

    def __str__(self) -> str:
        return self.error_message


class PollSchedule:
    """Defines everything what happenes during a Poll event"""

    async def start(pollobj: Poll):
        """Start-Phase:
        calls the PollEmbedSender.sendProgress() method, reacts with
        the voting Emoji's and goes to the progress-phaseof the 
        Schedule"""

        await PollEmbedSender.sendProgress(pollobj)

        for i in range(pollobj.ans_number):
            await pollobj.mess.add_reaction(pollobj.emojis[i])

        await PollSchedule.progress(pollobj)
    
    async def progress(pollobj: Poll):
        """Progress-Phase:
        Sleeps for the duration of Poll.time. If the poll lasts longer
        than 24 hours (and poll is in Thread) then it sends a message
        every 24 hours in the Thread to prevent the Thread from
        auto-archiving."""
        
        if type(pollobj.channel) is Thread:
            while(pollobj.time > 86400):
                pollobj.time -= 86400
                await sleep(86400)
                message = await pollobj.channel.send("Auto-dearchive message.")
                await message.delete()
        await sleep(pollobj.time)

        await PollSchedule.end(pollobj)

    async def end(pollobj: Poll):
        """End-Phase:
        Analyzes the results of the completed poll and gets the winner. Therefor it has to
        get the new Discord `Message` Object from disnake.utils"""

        #find index of answer option with most votes
        print(f"Poll '{pollobj.poll_name}' finished:")
        max = -1
        for i in pollobj.answer_options: 
            print(f"{i.name}: {i.votes - 1} votes")
            if i.votes > max:
                max = i.votes
                winner = pollobj.answer_options.index(i)
                
        await PollEmbedSender.sendResult(pollobj, winner)


class PollEmbed(Embed):
    """Defines basic format for all Embeds attached to the Poll Bot Function."""   
        
    def __init__(self, description: str) -> None:

        super().__init__()
        
        self.description = description
        self.colour = Colour(0x355326)
        self.timestamp = datetime.now()                


class PollEmbedSender:
    """All method definitions to send Embeds attached to the Poll Bot Function."""

    async def sendEmbed(message: str, channel: TextChannel | Thread):
        """Sends an PollEmbed with the given string to the given channel."""

        embed = PollEmbed(message)
        await channel.send(embed= embed)

    async def sendSetup(pollObj: Poll):
        """Sends an Embed in the Poll-Channel. It shows the Options of the Poll
        before starting the Event"""

        string =    f"\n**Current Settings:**\npoll name = '{pollObj.poll_name}'\n"\
                    f"time = {pollObj.time} seconds\nnumber of answers = "\
                    f"{pollObj.ans_number}\n\n**Current answer oprions:**\n"
        embed = PollEmbed(string)

        for i in range(pollObj.ans_number):
            embed.add_field(
                name= pollObj.emojis[i],
                value= pollObj.answer_options[i].name,
                inline= True
            )

        if pollObj.mess != None:
            await pollObj.mess.delete()
        pollObj.mess = await pollObj.channel.send(embed= embed)

    async def sendProgress(pollObj: Poll):
        """Sends the Embed which is shown while the Poll is active. It shows all
        given answer Options, a quick guide how to vote and the timestamp when the
        poll event will end."""
        
        time = datetime.now() + timedelta(seconds=float(pollObj.time))
        time = str(time)
        time = time.split(".")[0]

        string =    f"Active Poll:\n\nReact with one of the given Emoji's to vote. The "\
                    f"poll will end at {time}.\n\n**Answer Options are:**\n"
        embed = PollEmbed(string)

        for i in range(pollObj.ans_number):
            embed.add_field(
                name= pollObj.emojis[i],
                value= pollObj.answer_options[i].name,
                inline= True
            )

        await pollObj.mess.delete()
        pollObj.mess = await pollObj.channel.send(embed= embed)

    async def sendResult(pollObj: Poll, winner: int):
        """Sends the Embed which shows the result (winner) of the poll event. If the 
        channel in which the poll event takes place, is a Thread (usually should be so),
        then the Thread will be archived."""

        string =    f"**The Winner is drawn**\n\n{pollObj.answer_options[winner].name} "\
                    f"won the poll with {pollObj.answer_options[winner].votes-1} votes."
        
        embed = PollEmbed(string)

        await pollObj.mess.delete()
        pollObj.mess = await pollObj.channel.send(embed= embed)

        if type(pollObj.channel) is Thread:
            await pollObj.channel.edit(archived= True)
