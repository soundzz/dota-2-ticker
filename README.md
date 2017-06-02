# ticker
Dota 2 stalker xd

i am noob and have never done anything like this so excuse bad coding/bad handling on github LUL

This script periodically scans the match history of given accounts and notifies the user when one of those accounts finishes a match (player xy ahs finished a match with hero x and a score of k/d/a)

You still need to insert your own dota 2 api key in the .py file and modify the player_ids dictionary to list the accounts you want to track.

the script refreshes the data every 60 seconds

If you want the script to automatically run on startup, create a .bat in your autostart folder with the line:

start pythonw C:\{whatever path you saved the files in}\ticker.pyw

before running the script for the first time you will need to install the dota2api package ($pip install dota2api) and maybe the pypiwin32 package.
