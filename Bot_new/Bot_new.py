
import discord
from discord import client
from discord.ext import commands
from discord.ext.commands.context import Context
from discord import Message

from poll_new import Poll
from Bot.wiki import wiki_main

poll_dic = {}

client = commands.Bot(
    command_prefix="!",
    help_command= None
)

@client.event
async def on_ready():
    """Called when the Bot Client is logged in after the start."""

    print("Bot is online")
    await client.change_presence(activity=discord.Game("!help"), status=discord.Status.online)

@client.command(
    name="wiki",
    aliases=["Wiki", "wikipedia", "Wikipedia", "w", "W"],
    description= "Get the summary of the wikipedia article. (default language is german)",
    help= "wiki")
async def wiki(ctx: Context):
    await wiki_main(ctx.message)

@client.command(
    name="poll",
    aliases=["Poll", "p", "P"],
    description= "Command to create and setup a new Poll in a Text-Channel (Not DM-Channel)\n",
    help= "poll")
async def poll(ctx: Context, *args: str):

    if len(args) < 1 or len(args) > 2:
        return
    if args[0] == "create":
        if len(args) < 2:
            return
        await utils.create_poll(ctx.message)
    elif args[0] == "start":
        if len(args) > 1:
            return
        await utils.start_poll(ctx.message.channel.id)
    elif args[0] == "rename":
        if len(args) < 2:
            return
        utils.rename_poll(ctx.message.channel.id, args[1])
    elif args[0] == "time":
        if len(args) < 2:
            return
        utils.set_poll_time(ctx.message.channel.id, args[1])
    elif args[0] == "delete":
        if len(args) > 1:
            return
        await utils.delete_poll(ctx.message.channel.id)
    elif args[0] == "addans":
        pass
    elif args[0] == "delans":
        pass
    return



class utils:
    
    @staticmethod
    async def create_poll(message: Message):
        """Calls the poll-Constructor and stroes the object in the poll_dic with message id in which they're created"""

        if type(message.channel) is discord.DMChannel:
            await message.channel.send("The !poll feature is not available in DM-Channels.")
            return

        if str(message.channel.id) in poll_dic:
            await message.channel.send("There is already an existing poll in this channel. Wait until its finished or delete it if the poll has not started yet.")
            return

        try:
            value = int(message.content.split(" ", 2)[2])
        except ValueError:
            return
        
        if value > 11 or value < 2:
            await message.channel.send("The number of the answer options has to be between 2 and 11.")
            return

        new_poll = Poll(value)
        poll_dic[str(message.channel.id)] = new_poll
        await poll_dic[str(message.channel.id)].send_setup_Embed(message.channel)

    @staticmethod
    async def start_poll(channel_id: int):
        """starts the poll event of poll_obj, calls Poll.start and Poll.send_result_Embed"""

        try:
            poll_obj = poll_dic[str(channel_id)]
        except KeyError:
            return

        await poll_obj.start()
        send_msg = discord.utils.get(client.cached_messages, id=poll_obj.mess.id)
        await poll_obj.analyze_results(send_msg)
        del poll_dic[str(poll_obj.mess.channel.id)]

    @staticmethod
    def rename_poll(channel_id: int, new_name: str):
        """Changes the Poll.poll_name attribute of a Poll in the channel, if it exists."""

        try:
            poll_obj = poll_dic[str(channel_id)]
        except KeyError:
            return

        poll_obj.poll_name = new_name
        poll_obj.send_setup_embed()
        return

    @staticmethod
    def set_poll_time(channel_id: int, new_time: str):
        """Changes the Poll.time attribute of a Poll in the channel, if it exists."""

        try:
            poll_obj = poll_dic[str(channel_id)]
            new_time = int(new_time)
        except (KeyError, ValueError):
            return

        poll_obj.time = new_time
        poll_obj.send_setup_embed()
        return

    @staticmethod
    async def delete_poll(channel_id: int):
        """deletes an poll which is in the setup-phase."""
        
        await poll_dic[str(channel_id)].mess.delete()
        del poll_dic[str(channel_id)]
        return 

client.run("ODc5NzM4MzM0NzU3Mzg4Mzc4.YSUGKw.I0t9FBgfEvcPtcEVyoe5KbGF2-s")