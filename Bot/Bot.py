
import disnake
from disnake import ApplicationCommandInteraction, TextChannel, Thread, client
from disnake.ext import commands
from disnake.ext.commands.context import Context
from disnake import Message

from poll import Poll, PollError
from wiki import wiki_main, WIKI_DEFAULT_LANG

poll_dic: dict[str, Poll] = {} #all Poll objects are stored here
token = input("Bot-token:")

client = commands.Bot(
    command_prefix="!",
    help_command= None,
    intetns= disnake.Intents.default(),
    sync_commands_debug= True
)

@client.event
async def on_ready():
    """Called when the Bot Client is logged in after the start."""

    print("Bot is online")
    await client.change_presence(activity=disnake.Game("!help"), status=disnake.Status.online)

@client.command(
    name="wiki",
    aliases=["Wiki", "wikipedia", "Wikipedia", "w", "W"],
    description= "Get the summary of the wikipedia article. (default language is german)",
    help= "wiki")
async def wiki(ctx: Context, *args: str):
    if args[0].startswith("?"):
        lang = args[0].split("?")[1]
        args = args[1:]
        await ctx.send(embed= wiki_main(" ".join(args), lang))
    else:
        await ctx.send(embed= wiki_main(" ".join(args)))

@client.slash_command(
    description= "Get the summary of an wikipedia article.")
async def wiki(inter: ApplicationCommandInteraction, search_phrase: str, language: str= WIKI_DEFAULT_LANG):
    await inter.response.send_message(embed= wiki_main(search_phrase, language))

@client.command(
    name="poll",
    aliases=["Poll", "p", "P"],
    description= "Command to create and setup a new Poll in a Text-Channel (Not DM-Channel)\n",
    help= "poll")
async def poll(ctx: Context, *args: str):

    if args[0] == "create":
        if len(args) < 2:
            return
        args = args[1:]
        ctx.channel.send(embed=disnake.Embed(description="Created new Poll"))
        await utils.create_poll(ctx.message.channel, " ".join(args))
    elif args[0] == "start":
        if len(args) > 1:
            return
        await utils.start_poll(ctx.message.channel)
    elif args[0] == "rename":
        if len(args) < 2:
            return
        args = args[1:]
        await utils.rename_poll(ctx.message.channel, " ".join(args))
    elif args[0] == "time":
        if len(args) != 2:
            return
        await utils.set_poll_time(ctx.message.channel.id, args[1])
    elif args[0] == "delete":
        if len(args) > 1:
            return
        await utils.delete_poll(ctx.message.channel)
    elif args[0] == "addans":
        if len(args) < 2:
            return
        await utils.add_answer(ctx.message)
    elif args[0] == "delans":
        if len(args) != 2:
            return
        await utils.delete_answer(ctx.message)
    return

@client.slash_command(
    description= "Create a new poll."
)
async def poll(inter: ApplicationCommandInteraction, name: str, answer_number: int= 2, time: int= 60):

    await inter.response.send_message(embed=disnake.Embed(description="Created new Poll"))
    await utils.create_poll(channel= inter.channel, name= name, answer_number= answer_number, time= time)

@client.command(
    name="help",
    description="Get help for all commands this Bot understands.")
async def help(ctx: Context):
    await ctx.channel.send(embed=disnake.Embed(description="""!wiki (?[lang_acronym]) [search_phrase] --> get the summary of the wikipedia article (default language is german)\n
!poll create [name]             --> create a poll with a name
!poll start                     --> start the poll
!poll rename [name]             --> rename the poll
!poll time [time_in_seconds]    --> set the lasting time of the poll
!poll delete                    --> delete the poll
!poll addans [name]             --> add a new answer option
!poll delans [answer_index]     --> delete an answer option by index

All Commands are supported by Discord Slash-Commands.

Please report any Bugs on [GitHub](https://github.com/Looby72/PollBot/issues)."""))


class utils:
    """This class defines all static methods to "communicate" with the Poll class"""
    
    @staticmethod
    async def create_poll(channel: TextChannel | Thread, name: str, answer_number: int = 0, time: int = 60):
        """Calls the poll-Constructor and stroes the object in the poll_dic[Thread.id] (every poll creates a new thread)"""

        if not (type(channel) is TextChannel):
            await channel.send("This command is only avaliable in normal Guild-Text-Channels")
            return

        thread = await channel.create_thread(name= f"Poll '{name}'", type=disnake.ChannelType.public_thread, auto_archive_duration= 1440)
        
        new_poll = Poll(name= name, channel= thread, ans_number= answer_number, time= time)
        poll_dic[str(thread.id)] = new_poll
        await poll_dic[str(thread.id)].send_setup_Embed()

    @staticmethod
    async def start_poll(channel: TextChannel | Thread):
        """starts the poll event of poll_obj, calls Poll.start and Poll.send_result_Embed"""

        try:
            poll_obj = poll_dic[str(channel.id)]
        except KeyError:
            return

        try:
            await poll_obj.start()
        except PollError as error:
            await channel.send(str(error))
            return

        send_msg = disnake.utils.get(client.cached_messages, id=poll_obj.mess.id)
        await poll_obj.analyze_results(send_msg)
        del poll_dic[str(poll_obj.mess.channel.id)]

    @staticmethod
    async def rename_poll(channel: TextChannel | Thread, new_name: str):
        """Changes the Poll.poll_name attribute of a Poll in the channel, if it exists."""

        try:
            poll_obj = poll_dic[str(channel.id)]
        except KeyError:
            return

        if type(channel) is Thread:
            await channel.edit(name= f"Poll '{new_name}'")
        poll_obj.poll_name = new_name
        await poll_obj.send_setup_Embed()
        return

    @staticmethod
    async def set_poll_time(channel_id: int, new_time: str):
        """Changes the Poll.time attribute of a Poll in the channel, if it exists."""

        try:
            poll_obj = poll_dic[str(channel_id)]
            new_time = int(new_time)
        except (KeyError, ValueError):
            return

        poll_obj.time = new_time
        await poll_obj.send_setup_Embed()
        return

    @staticmethod
    async def delete_poll(channel: TextChannel | Thread):
        """deletes an poll which is in the setup-phase."""
        
        if type(channel) is Thread:
            await channel.delete()
        else:
            await poll_dic[str(channel.id)].mess.delete()
        del poll_dic[str(channel.id)]
        
        return 

    @staticmethod
    async def add_answer(message: Message):
        """Adds an answer to the poll in the channel of ``message``."""

        try:
            poll_obj = poll_dic[str(message.channel.id)]
        except KeyError:
            return

        answer = message.content.split(" ", 2)[2]
        await poll_obj.new_ans_op(answer)
        await poll_obj.send_setup_Embed()

    @staticmethod
    async def delete_answer(message: Message):
        """Deletes an answer option by index of the poll in the channel of ``message``"""
        
        try:
            poll_obj = poll_dic[str(message.channel.id)]
        except KeyError:
            return
        
        value = message.content.split(" ", 2)[2]

        try:
            value = int(value)
            await poll_obj.del_ans_op(value)
        except ValueError:
            return
        
        await poll_obj.send_setup_Embed()

client.run(token)