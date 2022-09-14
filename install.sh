rm -rf Bot
mkdir Bot
cd Bot
wget https://raw.githubusercontent.com/Looby72/PollBot/new-command-structure/Bot/Bot.py
wget https://raw.githubusercontent.com/Looby72/PollBot/new-command-structure/Bot/poll.py
wget https://raw.githubusercontent.com/Looby72/PollBot/new-command-structure/Bot/wiki.py
wget https://raw.githubusercontent.com/Looby72/PollBot/new-command-structure/Bot/operations.py
python3.10 -m pip install -U disnake
python3.10 -m pip install wikipedia