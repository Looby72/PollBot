#disnake imports
import disnake
from disnake import ApplicationCommandInteraction, Reaction, User, client
from disnake.ext import commands
from disnake.ext.commands.context import Context
#wiki imports
from wiki import wiki_main, WIKI_DEFAULT_LANG
#poll imports
from operations import PollOperations
from poll import PollEmbed

token = input("Bot-token:")
intents = disnake.Intents.default()
intents.typing = False #better performance since typing event is very spammy
intents.members = True #for on_reaction_add()
intents.message_content = True #for command prefix

client = commands.Bot(
    command_prefix="!",
    help_command= None,
    intetns= intents, #TODO get Intents.members (for on_reaction_remove) and Intents.reactions
    sync_commands_debug= True
)

@client.event
async def on_ready():
    """Called when the Bot Client is logged in after the start."""

    print("Bot is online")
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

    await inter.response.send_message(embed= PollEmbed("Created new Poll."))
    await PollOperations.createPoll(channel= inter.channel, name= name, answer_number= answer_number, time= time)

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


client.run(token)