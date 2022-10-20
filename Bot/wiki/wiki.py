"""Defines all Functions which are needed to realize the !wiki command of the Bot"""
#disnake imports
from disnake import Embed, Colour
#datetime imports
from datetime import datetime
#wikipedia imports
import wikipedia
from wikipedia.wikipedia import WikipediaPage
from wikipedia import WikipediaException

WIKI_DEFAULT_LANG = "en"

def wiki_main(search_phrase: str, lang: str= WIKI_DEFAULT_LANG) -> Embed:
    """Entry method of the wiki module, takes search-phrase and language and returns the discord Embed"""
    
    try:    
        lang_param(lang)
        embed = get_embed(search_phrase)
    except (WikipediaException , WikiLanguageError) as err:
        embed = WikiEmbed(description= str(err), title= type(err).__name__)
    
    return embed


def lang_param(langval: str):
    """Checks if the language parameter exists and sets the language in wikipedia"""

    if langval in wikipedia.languages():
        wikipedia.set_lang(langval)
    else:
        raise WikiLanguageError("Language '" + langval + "' not supported.")

def get_embed(searchval: str):
    """Returns the disnake.embed-object (formatted) to show the wikipedia-summary"""

    embed = None
    page = get_page(searchval)

    if page == None:
        description = "No Wikikedia article found, based on your search phrase :("
        title = "Error"
        embed = WikiEmbed(description= description, title= title)
    else:
        string = get_formatted_summary(page)
        description = string
        title = page.title
        thumbnail = get_picture_url(page)

        embed = WikiEmbed(description= description, title= title)

        if thumbnail != None:
            embed.set_thumbnail(url=thumbnail)

    return embed

def get_page(keyword: str) -> WikipediaPage | None:
    """Uses wikipedia search to return the best wikipedia page-object. Returns `None` if nothing was found, based on
    the keyword."""

    try:
        title = wikipedia.search(keyword)[0]
    except IndexError:
        return None

    return wikipedia.page(title=title, auto_suggest=False)

def get_formatted_summary(page: WikipediaPage):
    """Returns the formatted summary in the right length (character Limit of 4096 for Discord-embeds, 10 sentences)
    and with an embedded link to the orgiginal wikipedia article"""

    string = page.summary
    string = string + "\n[original article](" + page.url + ")"

    sentence_num = 10
    while len(string) > 4096:
        string = wikipedia.summary(title=page.title, sentences=sentence_num) + "\n[original Artikel](" + page.url + ")"
        sentence_num -= 1
    
    return string

def get_picture_url(page: WikipediaPage):
    """Returns the url of the first picture in the wikipedia.page.images list or None if the list is empty"""

    pictures = page.images
    if len(pictures) > 0:
        return pictures[0]
    else: return None

class WikiEmbed(Embed):
    """Defines basic format for all Embeds attached to the Wiki Bot Function."""   
        
    def __init__(self, description: str, title: str = "") -> None:

        super().__init__()
        
        self.description = description
        self.colour = Colour(0xcacfc9)
        self.timestamp = datetime.now()
        self.title = title

class WikiLanguageError(Exception):
    """Custom Exception-Class. Thrown, when invalid language prefix is passed."""

    def __init__(self, error: str) -> None:
        self.error_message = error

    def __str__(self) -> str:
        return self.error_message