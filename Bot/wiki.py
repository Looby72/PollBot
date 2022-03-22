"""Defines all Functions which are needed to realize the !wiki command of the Bot"""

import disnake
import wikipedia
import datetime
from wikipedia.wikipedia import WikipediaPage

WIKI_DEFAULT_LANG = "de"

def wiki_main(search_phrase: str, lang= WIKI_DEFAULT_LANG):
    """Entry method of the wiki module, takes search-phrase and language and returns the discord Embed"""
    
    try:    
        lang_param(lang)
        embed = get_embed(search_phrase)
    except Exception as err:
        embed = disnake.Embed(title = "Error", description = str(err), color = 0xcacfc9, timestamp=datetime.datetime.now())
    
    return embed


def lang_param(langval: str):
    """Checks if the language parameter exists and sets the language in wikipedia"""

    if langval in wikipedia.languages():
        wikipedia.set_lang(langval)
    else:
        raise Exception("Language '" + langval + "' not supported")

def get_embed(searchval: str):
    """Returns the disnake.embed-object (formatted) to show the wikipedia-summary"""

    page = get_page(searchval)
    string = get_formatted_summary(page)
    embed = disnake.Embed(title = page.title, description = string, color = 0xcacfc9, timestamp=datetime.datetime.now())
    thumbnail = get_picture_url(page)
    if thumbnail != None:
        embed.set_thumbnail(url=thumbnail)

    return embed

def get_page(keyword: str):
    """Uses wikipedia search to return the best wikipedia page-object"""

    title = wikipedia.search(keyword)[0]
    return wikipedia.page(title=title, auto_suggest=False)

def get_formatted_summary(page: WikipediaPage):
    """Returns the formatted summary in the right length (character Limit of 4096 for Discord-embeds, 10 sentences)
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