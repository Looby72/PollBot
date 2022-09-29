#disnake imports
from disnake import Embed, Colour
#datetime imports
from datetime import datetime
#enum imports
from enum import Enum

PAGE0 = """This bot supports 2 Commands:
`!wiki` sends a Wikipedia article summary from a given search phrase.
With `!poll` and its subcommands you can create polls in the discord chat and modify its settings.

Note that both commands have their own discord slash-command.

For more specific help type `!help` `command` or simply use `/help` `command`."""
PAGE1 = """The `!wiki` command uses the wikipedia search to provide you a matching Wikipedia article summary. On the bottom of every summary you can find a direct link to the found article.

__Syntax:__
`!wiki` `?lang_prefix` `search_phrase`

After `!wiki` you only have to type the `search_phrase` you're looking for.
This command also supports searching in different languages by adding `?lang_prefix` before the `search_phrase`. A list to all Wikipedia language prefixes can be found [here](https://meta.wikimedia.org/wiki/List_of_Wikipedias#All_Wikipedias_ordered_by_number_of_articles). 
Note that this command also works without the `lang_prefix`. Then the language will be english. You can also type in more than one word as `search_phrase`.

__Slash Command:__
This command also has an Discord slash command syntax. Just type `/wiki`. The Syntax is similar to the normal chat command.

__Errors:__
In case of an error either the Wikipedia API produced an error, or Wikipedia didn't find anything at all based on your search phrase."""
PAGE2 = """With the `!poll` command you can create multiple polls with a maximum of 11 answer options and different amounts of time in the text chat of your discord sever. After creating a poll the bot will create a new Thread where you can change settings of your poll and where the poll event will take place.

__Syntax:__
This command is devided into multiple subcommands:

`!poll` `create` `name`
creates a new poll with a given display name, this command only wokrs in normal text channels, not in threads.

`!poll` `rename` `name`
`!poll` `time` `time_in_secs`
`!poll` `addans` `ans_name`
`!poll` `delans` `ans_index`
These commands change the different settings of a created poll and they'll only work in a thread attached to an created poll. The current settings will always be displayed in the respective thread. Note that every poll has default settings, so every poll event will work without adjusting its settings.

`!poll` `delete`
will delete an created poll and will also delete the thread attached to the poll. This command only works in threads with a non active poll.

`!poll` `start`
will start the poll event which is over after the time given in the settings. While the event is active everyone on the server who has access to the thread can react to the poll message to vote. The bot will react on the message with all given emojis at the start of the event. When the event is over the winning answer option will be displayed.

__Slash Command:__
This command also supports Discord slash commands. With `/poll` `name` you can create a poll with a given display name. Optional you can already give the poll settings `name`,`answer_number` and `time` to create a custom poll with only one comand. Everything else cannot be done with slash commands and have to be done with the normal chat commands which are given above."""

pages = [PAGE0, PAGE1, PAGE2]
titles = ["Welcome to the Help Pages", "Wiki", "Poll"]

class HelpEmbed(Embed):
    """Defines basic format for all Embeds attached to the Help Bot Function."""

    def __init__(self, description: str, title: str) -> None:

        super().__init__()
        
        self.description = description
        self.title = title
        self.colour = Colour(0xe7caa9)
        self.timestamp = datetime.now()
        self.description += "\n\nPlease report any Bugs on [GitHub](https://github.com/Looby72/PollBot/issues)."

class HelpCommand:
    """Defines all methods implementing the Help command"""

    def get_help_embed(page: int) -> HelpEmbed | None:
        """Returns the help Text as `HelpEmbed` from a given page. `page` must be
        an int between 0 and 2, if not this mathod will return `None`"""

        if page > 2 or page < 0:
            return None
        return HelpEmbed(pages[page], titles[page])

class Page(int, Enum):

    introduction = 0
    wiki = 1
    poll = 2