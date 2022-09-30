# PollBot
A Discord Bot written in Python (disnake library). Current features are: Showing wikipedia Summaries and creating Polls in the Chat. 

## Installation (Linux):

- Install Python 3.10 (tested in 3.10.4)
- Install Python libraries disnake (at least version 2.5) and wikipedia
```console
python3.10 -m pip install -U disnake
```
```console
python3.10 -m pip install wikipedia
```
- download install.sh from the release page and put it in any directory you want (example with version v0.3)
```console
curl -L https://github.com/Looby72/PollBot/releases/download/v0.3/install.sh -o install.sh
```
- set execute permission
```console
chmod +x install.sh
```
- execute the script, it will download the necessary files and unpack them
```console
./install.sh
```
- to run the Bot execute the python file Bot.py in the new directory 'Bot'
```console
python3.10 Bot.py
```