
import discord
from discord.message import Message
from discord.reaction import Reaction
from discord.user import User
import wiki
from poll import Poll

class MyClient(discord.Client):
    """Represents the Bot-Client"""

    def __init__(self):
        discord.Client.__init__(self)
        self.poll_dic = {}
        self.help_text = "!wiki (?[Sprachkürzel]) [Suchbegriff] --> Wikipediazusammenfassung des Suchbegriffes in gewünschter Sprache (standardmäßig deutsch)"

    async def on_ready(self):
        """Called when the Bot Client is logged in after the start."""

        print("Bot is online")
        await self.change_presence(activity=discord.Game("!help"), status=discord.Status.online)
    
    async def on_message(self, message: Message):
        """Called when a message is posted in a channel which the bot can read."""

        if message.author == self.user:
            return
        elif message.content.startswith("!wiki "):
            await wiki.wiki_main(message)
        elif message.content.startswith("!poll "):
            await self.create_poll(message)
        elif message.content == "!help":
            await message.channel.send(self.help_text)
        else:
            try:
                poll_obj = self.poll_dic[str(message.channel.id)]
                self.set_poll_value(poll_obj, message.content)
                await message.delete()
                await poll_obj.send_setup_Embed(message.channel)
            except:
                return

            
            
    async def on_reaction_add(self, reaction: Reaction, user: User):
        """Called when a reaction has been added to a message in a channel which the bot can read.
        (not called when message is not in internal message-chache of the Bot)"""

        if user == self.user:
            return

        try:
            poll_obj = self.poll_dic[str(reaction.message.channel.id)]
        except:
            return
        
        if reaction.message.id == poll_obj.mess.id:
            if reaction.emoji == "❌":
                await self.delete_poll(reaction.message.channel.id)
            else:
                await self.set_poll_status(poll_obj, reaction.emoji)
        
                    
    async def create_poll(self, message: Message):
        """Calls the poll-Constructor and stroes the object in the poll_dic with message id in which they're created"""

        try:
            value = int(message.content.split(" ", 1)[1])
        except:
            return
        
        new_poll = Poll(value)
        self.poll_dic[str(message.channel.id)] = new_poll
        await self.poll_dic[str(message.channel.id)].send_setup_Embed(message.channel)
    
    def set_poll_value(self, poll_obj: Poll, content: str):
        """reads the poll_status from the right poll-object and sets the value (depending on poll_status)"""
        
        status = poll_obj.poll_status

        if status == 0:
            return
        elif status == 1:
            poll_obj.time = int(content)
        elif status == 2:
            poll_obj.poll_name = content
        elif status > 2 and status < 14:
            i = status - 3
            poll_obj.answer_options[i] = content

    async def set_poll_status(self, poll_obj: Poll, emoji: str):
        """sets the poll status of poll_obj (depending on the given emoji)"""

        if emoji == "⏱":
            poll_obj.poll_status = 1      
        elif emoji == "✏":
            poll_obj.poll_status = 2     
        elif emoji == "✅":
            await self.start_poll(poll_obj)
        else:       
            for i in range(len(poll_obj.emoji_list)):
                if emoji == poll_obj.emoji_list[i]:
                    poll_obj.poll_status = i+3
    
    async def start_poll(self, poll_obj: Poll):
        """starts the poll event of poll_obj, calls Poll.start and Poll.send_result_Embed"""

        await poll_obj.start()
        send_msg = discord.utils.get(self.cached_messages, id=poll_obj.mess.id)
        await poll_obj.analyze_results(send_msg)
        del self.poll_dic[str(poll_obj.mess.channel.id)]

    async def delete_poll(self, channel_id):
        """deletes an poll which is in the setup-phase called when message recation with ❌"""
        
        await self.poll_dic[str(channel_id)].mess.delete()
        del self.poll_dic[str(channel_id)]

def main():
    client = MyClient()
    client.run("ODc5NzM4MzM0NzU3Mzg4Mzc4.YSUGKw.I0t9FBgfEvcPtcEVyoe5KbGF2-s")

if __name__ == '__main__':
    main()