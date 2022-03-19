
import disnake
from disnake import ApplicationCommandInteraction, client
from disnake.ext import commands
from disnake.ext.commands.context import Context
from disnake import Message

from poll import Poll
from wiki import wiki_main, WIKI_DEFAULT_LANG

poll_dic = {}
token = input("Bot-token:")

client = commands.Bot(
    command_prefix="{",
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
        await ctx.send(embed=wiki_main(" ".join(args)))

@client.slash_command(
    description= "Get the summary of the wikipedia article.")
async def wiki(inter: ApplicationCommandInteraction, search_phrase: str, language= WIKI_DEFAULT_LANG):
    await inter.response.send_message(embed=wiki_main(search_phrase, language))
    """
    Get the summary of the wikipedia article.

    Parameters
    ----------
    search_phrase: :class:`str`
        The term to search for
    language: :class:`str`
        The Wikipedia article language
    """

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
        await utils.rename_poll(ctx.message.channel.id, args[1])
    elif args[0] == "time":
        if len(args) < 2:
            return
        await utils.set_poll_time(ctx.message.channel.id, args[1])
    elif args[0] == "delete":
        if len(args) > 1:
            return
        await utils.delete_poll(ctx.message.channel.id)
    elif args[0] == "addans":
        if len(args) < 2:
            return
        await utils.add_answer(ctx.message)
    elif args[0] == "delans":
        if len(args) < 2:
            return
        await utils.delete_answer(ctx.message)
    return

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
!poll delans [answer_index]     --> delete an answer option by index\n
Please report any Bugs on [GitHub](https://github.com/Looby72/DiscordBot/issues)."""))


class utils:
    
    @staticmethod
    async def create_poll(message: Message):
        """Calls the poll-Constructor and stroes the object in the poll_dic with message id in which they're created"""

        if type(message.channel) is disnake.DMChannel:
            await message.channel.send("The !poll feature is not available in DM-Channels.")
            return

        if str(message.channel.id) in poll_dic:
            await message.channel.send("There is already an existing poll in this channel. Wait until its finished or delete it if the poll has not started yet.")
            return

        value = message.content.split(" ", 2)[2]
        
        new_poll = Poll(name=value, channel= message.channel)
        poll_dic[str(message.channel.id)] = new_poll
        await poll_dic[str(message.channel.id)].send_setup_Embed()

    @staticmethod
    async def start_poll(channel_id: int):
        """starts the poll event of poll_obj, calls Poll.start and Poll.send_result_Embed"""

        try:
            poll_obj = poll_dic[str(channel_id)]
        except KeyError:
            return

        await poll_obj.start()
        send_msg = disnake.utils.get(client.cached_messages, id=poll_obj.mess.id)
        await poll_obj.analyze_results(send_msg)
        del poll_dic[str(poll_obj.mess.channel.id)]

    @staticmethod
    async def rename_poll(channel_id: int, new_name: str):
        """Changes the Poll.poll_name attribute of a Poll in the channel, if it exists."""

        try:
            poll_obj = poll_dic[str(channel_id)]
        except KeyError:
            return

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
    async def delete_poll(channel_id: int):
        """deletes an poll which is in the setup-phase."""
        
        await poll_dic[str(channel_id)].mess.delete()
        del poll_dic[str(channel_id)]
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