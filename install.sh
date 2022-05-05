rm -rf Bot
mkdir Bot
cd Bot
wget https://raw.githubusercontent.com/Looby72/PollBot/new-command-structure/Bot/Bot.py
wget https://raw.githubusercontent.com/Looby72/PollBot/new-command-structure/Bot/poll.py
wget https://raw.githubusercontent.com/Looby72/PollBot/new-command-structure/Bot/wiki.py
python -m pip install pyinstaller
python -m pip install -U disnake
python -m pip install wikipedia
pyinstaller Bot.py