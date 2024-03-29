#disnake imports
import disnake
from disnake import ApplicationCommandInteraction, Reaction, User, client
from disnake.ext import commands
from disnake.ext.commands.context import Context
#wiki imports
from wiki.wiki import wiki_main, WIKI_DEFAULT_LANG
#poll imports
from poll.operations import PollOperations
from poll.classes import PollEmbed
#help imports
from help.help import HelpCommand, Page

#TODO
#customize bot presence (with button for server join, command overview etc.)

token = input("Bot-token:")
intents = disnake.Intents.all()
intents.typing = False #better performance since the typing event is very spammy
intents.presences = False


client = commands.Bot(
    command_prefix="!",
    help_command= None,
    intents= intents,
    sync_commands_debug= True
)

@client.event
async def on_ready():
    """Called when the Bot Client is logged in after the start."""

    print("Bot is online\n")
    await client.change_presence(activity=disnake.Game("!help"), status=disnake.Status.online)

@client.event
async def on_reaction_add(reaction: Reaction, user: User):
    """Callback for Users reacting on messages."""

    PollOperations.adjustVotes(reaction.message.channel.id, 1, reaction.emoji)

@client.event
async def on_reaction_remove(reaction: Reaction, user: User):
    """Callback for Users removing reactions from messages."""
    
    PollOperations.adjustVotes(reaction.message.channel.id, -1, reaction.emoji)

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

    await inter.response.defer(with_message= True)
    #because wiki_main method sometimes takes more than 3 Seconds to produce an output bcause of Wikipedia
    await inter.edit_original_message(embed= wiki_main(search_phrase, language))

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
        await PollOperations.createPoll(ctx.message.channel, " ".join(args))
    elif args[0] == "start":
        if len(args) > 1:
            return
        await PollOperations.startPoll(ctx.message.channel)
    elif args[0] == "rename":
        if len(args) < 2:
            return
        args = args[1:]
        await PollOperations.renamePoll(ctx.message.channel, " ".join(args))
    elif args[0] == "time":
        if len(args) != 2:
            return
        await PollOperations.setPollTime(ctx.message.channel.id, args[1])
    elif args[0] == "delete":
        if len(args) > 1:
            return
        await PollOperations.deletePoll(ctx.message.channel)
    elif args[0] == "addans":
        if len(args) < 2:
            return
        await PollOperations.addAnswer(ctx.message)
    elif args[0] == "delans":
        if len(args) != 2:
            return
        await PollOperations.deleteAnswer(ctx.message)
    return

@client.slash_command(
    description= "Create a new poll."
)
async def poll(inter: ApplicationCommandInteraction, name: str, answer_number: int= 2, time: int= 60):
    
    output = await PollOperations.createPoll(channel= inter.channel, name= name, answer_number= answer_number, time= time)
    if output == 1:
        message = "Created Poll in a new Thread."
    elif output == 0:
        message = "Sorry!\nThis command is only available in normal Guild-Text-Channels."
    else:
        message = "Some error occured :("

    await inter.response.send_message(embed= PollEmbed(message))

@client.command(
    name="help",
    aliases=["Help", "h", "H"],
    description="Get help for all commands this Bot understands.")
async def help(ctx: Context, page: int | str = 0):
    
    if type(page) is str:
        string = page.lower()
        await ctx.send(embed=HelpCommand.get_help_embed(Page[string].value))
    else:
        await ctx.send(embed=HelpCommand.get_help_embed(page))

@client.slash_command(
    description="Get help for all commands this Bot understands."
)
async def help(inter: ApplicationCommandInteraction, page: Page = 0):

    await inter.response.send_message(embed= HelpCommand.get_help_embed(page))

client.run(token)