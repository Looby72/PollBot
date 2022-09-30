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
- download install.sh from this repository and put it in any directory you want (installation will be there) 
```console
wget https://raw.githubusercontent.com/Looby72/PollBot/new-command-structure/install.sh
```
- set execute permission
```console
chmod +x install.sh
```
- execute the script, it will install wikipedia and disnake python libraries and pyinstaller
```console
./install.sh
```
- to run the Bot execute the python file Bot.py in the directory 'Bot'
```console
cd Bot
```
```console
python3.10 Bot.py
```