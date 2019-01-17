# Ticker v2.0
Dota 2 Ticker

Well here i am, reworking this script almost 2 years later!
The core funcionality is still the same: You enter player Nicknames and (dotabuff) IDs, run the script in the background and will get a Notification every time one of those friends finish a match (including some detailed info about the match). This only works if that player has enabled public match history of course. The ticker script is ticker.py, the script used to set up API Key and player IDs is config.py

# How to set it up
1) Python 3 is required, so make sure you have it installed and linked the interpreter in your PATH Variable
2) all needed dependencies should be listed in requirements.txt and can be installed by running "pip install -r requirements.txt" inside the directory (in case there are uninstalled dependencies that are not listed in the requirements.txt, you will have to install the manually)
3) You will need a Dota 2 API Key. To obtain this go to https://steamcommunity.com/dev/apikey
4) After completing steps 1-3, you should first run config.py to set up the API key and the Player list
5) You are now ready to run ticker.py! If you run it with pyw ticker.py (or pythonw ticker.py) you can close the console window without killing the process (you will have to kill it using Task manager/shutting down your computer)
OPTIONAL:
6) creating a .bat file in the directory containing the line "start pyw {directory path}\ticker.py" will give you a simple way to start the script by double clicking it (same way for config.py)

# Whats new?
-GUI for entering API Key and Player IDs (in config.py)
-log file keeping track of the finished matches in the current session including dotabuff links (and more info about program execution)
-a whole lot of error handling to avoid the script crashing on you with incomprehensible error messages when entering invalid keys/player IDs  or IDs of players with a private profile 

# Bugs?
With this version there are probably bugs that i haven't thought of when testing my application, so please let me know by either opening an issue here or messaging me on reddit at /u/FeIiix
