rm -rf Bot
mkdir Bot
cd Bot
wget https://raw.githubusercontent.com/Looby72/DiscordBot/new-command-structure/Bot/Bot.py
wget https://raw.githubusercontent.com/Looby72/DiscordBot/new-command-structure/Bot/poll.py
wget https://raw.githubusercontent.com/Looby72/DiscordBot/new-command-structure/Bot/wiki.py
pip install pyinstaller
python3 -m pip install -U disnake
pyinstaller --onefile Bot.py