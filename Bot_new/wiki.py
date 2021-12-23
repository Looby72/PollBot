"""Defines all Functions which are needed to realize the !wiki command of the Bot"""

from discord.message import Message
import wikipedia
import discord
import datetime
from wikipedia.wikipedia import WikipediaPage

WIKI_DEFAULT_LANG = "de"

async def wiki_main(message: Message):
    """Realizes the wiki feature of the Bot (entry function)"""

    command_params = message.content.split(" ", 1)[1]
    
    try:
        if command_params.startswith("?"):
            searchval = lang_param(command_params)
        else:
            wikipedia.set_lang(WIKI_DEFAULT_LANG)
            searchval = command_params
            
        embed = get_embed(searchval)
    except Exception as err:
        embed = discord.Embed(title = "Error", description = str(err), color = 0xcacfc9, timestamp=datetime.datetime.utcnow())
    
    await message.channel.send(embed=embed)


def lang_param(content: str):
    """Checks and splits the language parameter from 'content' and sets the language for the wikipedia search"""

    searchval = content.split(" ", 1)[1]
    langval = content.split(" ", 1)[0].replace("?", "")

    if langval in wikipedia.languages():
        wikipedia.set_lang(langval)
    else:
        raise Exception("Language '" + langval + "' not supported")
    
    return searchval

def get_embed(searchval: str):
    """Returns the Discord.embed-object (formatted) to show the wikipedia-summary"""

    page = get_page(searchval)
    string = get_formatted_summary(page)
    embed = discord.Embed(title = page.title, description = string, color = 0xcacfc9, timestamp=datetime.datetime.utcnow())
    thumbnail = get_picture_url(page)
    if thumbnail != None:
        embed.set_thumbnail(url=thumbnail)

    return embed

def get_page(keyword: str):
    """Uses wikipedia search to return the best wikipedia page-object"""

    title = wikipedia.search(keyword)[0]
    return wikipedia.page(title=title, auto_suggest=False)

def get_formatted_summary(page: WikipediaPage):
    """Returns the formatted summary in the right length (character Limit of 4096 for discord-embeds, 10 sentences)
    and with an embedded link to the orgiginal wikipedia article"""

    string = page.summary
    string = string + "\n[original Artikel](" + page.url + ")"

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