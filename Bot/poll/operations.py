#classes imports
from poll.classes import Poll, PollError, PollEmbedSender
#disnake imports
import disnake
from disnake import TextChannel, Thread, Message

poll_dic: dict[str, Poll] = {} #all Poll objects are stored here

class PollOperations:
    """defines all functions to implement the bot poll commands"""

    def getPollObj(id: int) -> Poll | None:
        """Get the Poll object from the poll_dic by id (=channel_id in which the poll was created)"""
        
        try:
            poll_obj = poll_dic[str(id)]
        except KeyError:
            return None
        
        return poll_obj

    async def createPoll(channel: TextChannel | Thread, name: str, answer_number: int = 0, time: int = 60) -> int:
        """Calls the poll-Constructor and stroes the object in the poll_dic[Thread.id]
        (every poll creates a new thread)"""
        
        if not (type(channel) is TextChannel):
            return 0

        thread = await channel.create_thread(
            name= f"Poll '{name}'",
            type=disnake.ChannelType.public_thread,
            auto_archive_duration= 1440)
        
        new_poll = Poll(name= name, channel= thread, ans_number= answer_number, time= time)
        poll_dic[str(thread.id)] = new_poll
        await PollEmbedSender.sendSetup(new_poll)

        return 1

    async def startPoll(channel: TextChannel | Thread):
        """Gets the Poll Object and calls Poll.start to start the event schedule."""
        
        pollobj = PollOperations.getPollObj(channel.id)
        if pollobj == None:
            return

        try:
            await pollobj.start()
        except PollError as e:
            await PollEmbedSender.sendEmbed(str(e), channel)

    async def renamePoll(channel: TextChannel | Thread, new_name: str):
        """Changes the Poll.poll_name attribute of a Poll in the channel, if it exists."""

        pollobj = PollOperations.getPollObj(channel.id)
        if pollobj == None:
            return
        
        if type(channel) is Thread:
            await channel.edit(name= f"Poll '{new_name}'")
        pollobj.poll_name = new_name
        await PollEmbedSender.sendSetup(pollobj)

    async def setPollTime(channel_id: int, new_time: str):
        """Changes the Poll.time attribute of a Poll in the channel, if it exists."""

        pollobj = PollOperations.getPollObj(channel_id)
        if pollobj == None:
            return

        try:
            new_time = int(new_time)
        except (ValueError):
            await PollEmbedSender.sendEmbed(
                "Please give an Integer value for the new time.",
                pollobj.channel
                )
            return

        pollobj.time = new_time
        await PollEmbedSender.sendSetup(pollobj)

    async def deletePoll(channel: TextChannel | Thread):
        """deletes an poll which is in the setup-phase."""
        
        pollobj = PollOperations.getPollObj(channel.id)
        if pollobj == None:
            return

        await pollobj.mess.delete()
        del pollobj

        if type(channel) is Thread:
            await channel.delete()

    async def addAnswer(message: Message):
        """Adds an answer to the poll in the channel of `message`."""

        pollobj = PollOperations.getPollObj(message.channel.id)
        if pollobj == None:
            return

        answer = message.content.split(" ", 2)[2]

        try:
            pollobj.add_answer(answer)
        except PollError as e:
            await PollEmbedSender.sendEmbed(str(e), message.channel)

        await PollEmbedSender.sendSetup(pollobj)

    async def deleteAnswer(message: Message):
        """Deletes an answer option by index of the poll in the channel of `message`"""
        
        pollobj = PollOperations.getPollObj(message.channel.id)
        if pollobj == None:
            return
        
        value = message.content.split(" ", 2)[2]

        try:
            value = int(value)
            await pollobj.delete_answer(value)
        except ValueError:
            await PollEmbedSender.sendEmbed(
                "Please give an Integer value for the index of the answer to delete.",
                message.channel
                )
            return
        except PollError as e:
            await PollEmbedSender.sendEmbed(str(e), message.channel)
        
        await PollEmbedSender.sendSetup(pollobj)

    def adjustVotes(id: int, toAdd: int, emoji: str):
        """Adjusts the votes from an Answer Opion in an Poll Object. toAdd should be
        1 or -1, id should be the channel_id of the poll, emoji should be the emoji
        of the Answer Option."""

        pollobj = PollOperations.getPollObj(id)

        if pollobj == None:
            return
        
        if emoji in pollobj.emojis:
            index = pollobj.emojis.index(emoji)
            pollobj.answer_options[index].votes += toAdd



        