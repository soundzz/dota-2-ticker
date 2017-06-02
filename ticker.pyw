import dota2api
from win32api import *
from win32gui import *
import win32con
import sys, os
import struct
import time



api = dota2api.Initialise('api key') #insert your api key here

player_ids = {'playerid12345' : 'playername'} #edit this with the accoutns you want to track

class WindowsBalloonTip:
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

def showInfo(player_id, match_id):
	match = api.get_match_details(match_id=match_id)
	hero = ''
	kda = ''
	winOrLose = 'lost'
	minutes = match['duration'] // 60
	seconds = match['duration'] - minutes * 60
	duration = str(minutes) + ':' + str(seconds)
	for player in match['players']:
		if(player['account_id']==player_id):
			isRadiant = (player['player_slot'] < 128)
			if isRadiant == match['radiant_win']:
				winOrLose = 'won'
			hero = player['hero_name']
			kda = str(player['kills']) + '/' + str(player['deaths']) + '/' + str(player['assists'])

	w.ShowWindow('New match!', player_ids[str(player_id)] + ' just ' + winOrLose + ' a ' + duration + ' match as ' + hero + ' with a K/D/A of ' + kda)

#initialisation
w = WindowsBalloonTip()


game_lists = {}
for id in player_ids:
	history = api.get_match_history(account_id = id)
	gamelist = []
	for game in history['matches']:
		gamelist.append(game['match_id'])
	game_lists[id] = gamelist	 

w.ShowWindow('Initialisation succesful', 'Match history loaded')
#initialisation end

while True:
    for id in player_ids:
        history = api.get_match_history(account_id = id)
        for game in history['matches']:
            if not game['match_id'] in game_lists[id]:
                showInfo(int(id), int(game['match_id']))
                game_lists[id].append(game['match_id'])
    time.sleep(60) #change this value if you want more/less frequent updates