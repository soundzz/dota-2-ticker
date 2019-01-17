import dota2api
from win32api import *
from win32gui import *
import win32con
import sys, os
import struct
import time
import csv

class WindowsBalloonTip: #class used to create the popup window
    def __init__(self):
        message_map = {
                win32con.WM_DESTROY: self.OnDestroy,
        }
        # Register the Window class.
        wc = WNDCLASS()
        self.hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        self.classAtom = RegisterClass(wc)

    def ShowWindow(self,title, msg):
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow( self.classAtom, "Taskbar", style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, self.hinst, None)
        UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join( sys.path[0], "balloontip.ico" ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
           hicon = LoadImage(self.hinst, iconPathName, \
                    win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
          hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, \
                         (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,\
                          hicon, "Balloon  tooltip",msg,200,title))
        # self.show_balloon(title, msg)
        time.sleep(10)
        DestroyWindow(self.hwnd)

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app..

def writeLog(logMessage): #method to write log entries
    log_writer = open("log.txt", "a")
    log_writer.write(time.strftime("%d/%m/%Y") +" "+ time.strftime("%H:%M:%S") + " | " + logMessage + "\n")
    log_writer.close()

def showInfo(player_id, match_id): #shows popup and creates log entry for the player-match pair (player_id, match_id)
    match = api.get_match_details(match_id=match_id)
    hero = ''
    kda = ''
    winOrLose = 'lost'
    minutes = match['duration'] // 60
    seconds = match['duration'] - minutes * 60
    duration = str(minutes) + ':' + str(seconds).zfill(2)
    for player in match['players']:
        if(player['account_id']==player_id):
            isRadiant = (player['player_slot'] < 128)
            if isRadiant == match['radiant_win']:
                winOrLose = 'won'
            hero = player['hero_name']
            kda = str(player['kills']) + '/' + str(player['deaths']) + '/' + str(player['assists'])
            
    writeLog(player_ids[str(player_id)] + ' just ' + winOrLose + ' a ' + duration + ' match as ' + hero + ' with a K/D/A of ' + kda + " | " + "www.dotabuff.com/matches/" + str(match_id))
    w.ShowWindow('New match!', player_ids[str(player_id)] + ' just ' + winOrLose + ' a ' + duration + ' match as ' + hero + ' with a K/D/A of ' + kda)

#initialisieren
w = WindowsBalloonTip()

log_writer = open("log.txt", "w")
log_writer.write(time.strftime("%d/%m/%Y") +" "+ time.strftime("%H:%M:%S") +  " | log initialized " + "\n") #initialize log
log_writer.close()

try: #try reading api key from file
    key_file = open("api.key", "r")
    key = key_file.read()
    key_file.close()
    writeLog("API Key loaded from file")
except FileNotFoundError: #if no file exists, prompt user to check log
    writeLog("API Key not found, run setup.py")
    w.ShowWindow("Error", "Initialization failed, check log.txt for details")
    exit()

try: #try reading player IDs from file
    player_ids = {}
    player_file = open('players.dict', 'r')
    csv_reader = csv.DictReader(player_file)
    player_ids = next(csv_reader)
    player_file.close()
    if not player_ids:
        raise FileNotFoundError
    writeLog("player list loaded from file")
except FileNotFoundError: #if no file found prompt user to check log. INCORRECT DATA FORMAT IN FILE NOT DETECTED
    writeLog("no player list found, enter player IDs with setup.py")
    w.ShowWindow("Error", "Initialization failed, check log.txt for details")
    exit()

try: #initialize api connection, test connection to verify key 
    api = dota2api.Initialise(key)
    match = api.get_match_details(match_id=743387385)
    writeLog("API Key verified")
except Exception: #if key invalid/no internet connection etc create log entry
    writeLog("API Initialization failed, invalid API Key?")
    w.ShowWindow("Error", "Initialization failed, check log.txt for details")
    exit()

game_lists = {} #used to store match histories of the players
invalid_ids = []
for id in player_ids: #check for accounts with private match data/invalid player IDs
    try:
        history = api.get_match_history(account_id = id)
        gamelist = []
        for game in history['matches']:
            gamelist.append(game['match_id'])
        game_lists[id] = gamelist
        writeLog("loaded match history for player " + player_ids[id] + " - " + str(id))
    except Exception: 
        writeLog("unable to load match history for player " + player_ids[id] + " - " + str(id) + ", invalid player ID/private match history?")
        invalid_ids.append(id)
for id in invalid_ids:
    del player_ids[id]

writeLog("excluding players with private match data from tracking")

#initialisieren ende
w.ShowWindow("Success", "Initialization successful!")

while True: #endless loop, executed once every minute
    for id in player_ids:
        history = api.get_match_history(account_id = id)
        for game in history['matches']:
            if not game['match_id'] in game_lists[id]: #if "new" history contains game not yet in game_lists[id] -> new match
                showInfo(int(id), int(game['match_id']))
                game_lists[id].append(game['match_id'])
    time.sleep(50) #+10 sec of inactivity when popup is showing