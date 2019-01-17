import os #for clearing console
import sys
from msvcrt import getch #key input
import csv

#Keycodes for better readability:
KEY_1 = 49
KEY_2 = 50
KEY_3 = 51
KEY_ESC = 27

cls = lambda: os.system('cls') #cls() to clear console 

def print_header():
    cls()
    print("---------------------------")
    print("|  Dota Ticker Setup v.1  |")
    print("---------------------------")

def main_menu():
    print_header()
    print("+-------------------------+")
    print("+ 1: Enter/Change API Key +")
    print("+-------------------------+")
    print("+ 2: Manage Player IDs    +")
    print("+-------------------------+")
    print("+ ESC: Exit               +")
    print("+-------------------------+")
    key = None
    while key not in [KEY_1, KEY_2, KEY_3, KEY_ESC]:
        key = ord(getch()) #1: 49, 2: 50, 3: 51
    if key == KEY_1:
        manage_api_key()
    elif key == KEY_2:
        manage_player_ids()
    elif key == KEY_ESC:
        exit()

def manage_api_key():
    print_header()
    try: #try opening file api.key
        api_file = open("api.key", "r")
        api_key = api_file.read() #read api key from file to api_key
        api_file.close()
        print("+-------------------------------------------------------+")
        print("+ Current API Key: ", api_key, " " * (34 - len(api_key)), "+")
        print("+-------------------------------------------------------+")
        print("+ 1: Enter new API Key                                  +")
        print("+-------------------------------------------------------+")
        print("+ ESC: Back                                             +")
        print("+-------------------------------------------------------+")
        key = None
        while key not in [KEY_1, KEY_ESC]:
            key = ord(getch())
        if key == KEY_1:
            enter_api_key()
        elif key == KEY_ESC:
            main_menu()
        
    except FileNotFoundError: #if no api.key is found, prompt user to set it up
        print("+----------------------------------------+")
        print("+ You do not have an API Key set up yet. +")
        print("+----------------------------------------+")
        print("+ 1: Enter API Key                       +")
        print("+----------------------------------------+")
        print("+ ESC: Back                              +")
        print("+----------------------------------------+")
        key = None
        while key not in [KEY_1, KEY_ESC]:
            key = ord(getch())
        if key == KEY_1:
            enter_api_key()
        if key == KEY_ESC:
            main_menu()

def enter_api_key():
    print_header()
    print("+---------------------------+")
    print("+ Enter your API Key below: +")
    print("+---------------------------+")
    api_key = input(">> ") #enter api key
    api_file = open("api.key", "w")
    api_file.write(api_key)
    api_file.close() #save api key to api.key file
    print_header()
    print("+----------------------------+")
    print("+ API Key saved successfully +")
    print("+----------------------------+")
    print("+ Any key for Main Menu      +")
    print("+----------------------------+")
    key = ord(getch())
    main_menu()

def manage_player_ids():
    print_header()
    try: #if players.dict exists and contains at least one valid entry, load dictionary to players_dict
        players_dict = {}
        player_file = open('players.dict', 'r')
        csv_reader = csv.DictReader(player_file)
        players_dict = next(csv_reader)
        player_file.close()
        
        if not players_dict:
            raise FileNotFoundError
        print("+----------------------------------------+")
        print("+ Player IDs loaded                      +")
        print("+----------------------------------------+")
        print("+ 1: Enter/Update player IDs             +")
        print("+----------------------------------------+")
        print("+ 2: Delete player IDs                   +")
        print("+----------------------------------------+")
        print("+ ESC: Back                              +")
        print("+----------------------------------------+")
        key = None
        while key not in [KEY_1, KEY_2, KEY_ESC]:
            key = ord(getch()) 
        if key == KEY_1:
            enter_player_ids(players_dict)
        elif key == KEY_2:
            edit_player_ids(players_dict)
        elif key == KEY_ESC:
            main_menu()
        
    except Exception: #if players.dict doesnt exist or is empty, prompt user to enter IDs
        print("+----------------------------------------+")
        print("+ You do not have any player IDs saved.  +")
        print("+----------------------------------------+")
        print("+ 1: Enter/Update player IDs             +")
        print("+----------------------------------------+")
        print("+ ESC: Back                              +")
        print("+----------------------------------------+")
        key = None
        while key not in [KEY_1, KEY_ESC]:
            key = ord(getch())
        if key == KEY_1:
            enter_player_ids({})
        elif key == KEY_ESC:
            main_menu() 

def enter_player_ids(players_dict):
    """
    @param players_dict: dictionary with player IDs + nicknames that will be updated/filled within this method
    """
    aborted = False
    while not aborted:
        print_header()
        print("+-----------------------------------------+")
        print("+ Enter new player name ('esc' to exit)   +")
        print("+-----------------------------------------+")
        player_name = input(">> ")
        if player_name == 'esc':
            aborted = True
        while player_name in players_dict.keys():
            print_header()
            print("+-----------------------------------------+")
            print("+ Name already exists. Enter player name: +")
            print("+-----------------------------------------+")
            player_name = input(">> ")
        if aborted != True:
            print("+-----------------------------------------+")
            print("+ Enter player ID for ", player_name, " "* (19-len(player_name)))
            print("+-----------------------------------------+")
            player_id = input(">> ")
            players_dict.update({player_id : player_name})
    #write player_ids to csv:
    player_file = open('players.dict', 'w')
    fileWriter = csv.DictWriter(player_file, players_dict.keys())
    fileWriter.writeheader()
    fileWriter.writerow(players_dict) 
    player_file.close()
    manage_player_ids()

def edit_player_ids(players_dict): 
    print_header()
    keys = list(players_dict.keys())

    for index in range(1, len(players_dict)+1):
        print(">> ", index, ":" ,players_dict[keys[index-1]],"|", keys[index-1])
    print("+----------------------------------------+")
    print("+ Enter indexes of IDs to delete:        +")
    print("+ e.g. '2 3 4' ('d_all') deletes all IDs +")
    print("+ empty query to cancel                  +")
    print("+----------------------------------------+")  
    query = str(input(">> "))
    if query == 'd_all':
        players_dict.clear()
    elif query == '':
        manage_player_ids()
    else:
        try:
            del_index = query.split()
            for i in del_index:
                del players_dict[keys[int(i)-1]]
        except Exception:
            print("+------------------------------------------+")
            print("+ Invalid Input. Press Any Key to continue +")
            print("+------------------------------------------+")
            key = ord(getch())
            edit_player_ids(players_dict)
    
    #write player_ids to csv:
    player_file = open('players.dict', 'w')
    fileWriter = csv.DictWriter(player_file, players_dict.keys())
    fileWriter.writeheader()
    fileWriter.writerow(players_dict) 
    player_file.close()
    edit_player_ids(players_dict)
    
#main program:
main_menu()