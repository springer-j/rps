#--------------------------------------------------------

# Title             # Rock, Paper, Scissors
# Date:             # 2/25/23
# Python Version:   # 3.10.9

#--------------------------------------------------------

import json
import sys
from subprocess import call
from random import randint
from time import sleep

#--------------------------------------------------------

data_file = "data.json"
move_list = {
    1:{
        "move_name":"ROCK",
        "loses_to":2 # Paper
    },
    2:{
        "move_name":"PAPER",
        "loses_to":3 # Scissors
    },
    3:{
        "move_name":"SCISSORS",
        "loses_to":1 # Rock
    }
}
#--------------------------------------------------------

def load_data():
    return json.load(open(data_file,"r"))


def save_data(new_data):
    with open(data_file, "w") as file:
        file.write(json.dumps(new_data,indent=4))

#--------------------------------------------------------

def clear():
    call("clear")


def line():
    print("-" * 50)


def quit():
    clear()
    sys.exit()

#--------------------------------------------------------
#? Profile Management

def create_profile():
    clear()
    data = load_data()
    start_bal = data["settings"]["start_bal"]
    print("[!] Creating new profile\n")
    profile_name = input("[?] Your name: ")
    print("[!] Your starting balance will be $" + str(start_bal))
    conf = input("\n[?] Confirm? (Y/N) ")
    while conf.lower() != "y" and conf.lower() != "n":
        conf = input("\n[?] Confirm? (Y/N) ")
    if conf.lower() == 'y':
        profile = {
            "name":profile_name,
            "balance":start_bal,
            "bet":0,
            "wins":0,
            "losses":0,
            "busts":0
        }
        data["profiles"].append(profile)
        save_data(data)
        print(f"\n[!] Profile for {profile_name} saved.")
        input("[!] Press enter to continue.")
        return 
    elif conf.lower() == 'n':
        print("\n[X] Profile skipped.")
        input("[!] Press enter to continue.")
        return


def select_profile():
    #! Going to need some exception handling on this one
    data = load_data()
    profile_list = data["profiles"]
    if not profile_list:
        clear()
        print("[X] No profiles detected.")
        print("[X] You have to select a profile to play!")
        conf = input("\n[?] Create one now? (Y/N) ")
        if conf.lower() != "y" and conf.lower() != "n":
            conf = input("\n[?] Create one now? (Y/N) ")
        if conf.lower() == 'y':

            create_profile()
            select_profile()
        elif conf.lower() == 'n':
            return 
    clear()
    print("[!] Select a profile from the list")
    # Display numbered list for user to pick from
    # User input as the index value from profile_list
    for name in profile_list:
        print(f"[{str(profile_list.index(name) + 1)}]. {name['name']}")
    select = input("\n[?] ")
    return profile_list[int(select) - 1]


def refresh_profile(player):
    # Find "player" in JSON, return player dict
    # Used when changing JSON values during runtime
    data = load_data()
    for profile in data["profiles"]:
        if profile["name"] == player["name"]:
            return profile
    

def change_bet(player):
    data = load_data()
    for prof in data["profiles"]:
        if prof["name"] == player["name"]:
            profile = prof
    clear()
    print("[!] Changing bet\n")
    print("[!] Current bet: $" + str(profile['bet']))
    print("[!] Current balance: $" + str(profile['balance']))
    new_bet = int(input("\n[?] New bet: $"))
    while new_bet > profile['balance']:
        print("\n[X] Too broke for that.")
        new_bet = int(input("\n[?] New bet: $"))
    profile["bet"] = new_bet
    save_data(data)


def profile_management_menu():
    while True:
        clear()
        print("[1]. View profiles")
        print("[2]. Add profiles")
        print("[3]. Delete profiles")
        print("[4]. Return to menu")
        select = input("\n[?] ")
        if select == '1':
            input("wip") 
        elif select == '2':
            create_profile()
        elif select == '3':
            input("wip")
        elif select == '4':
            return

#--------------------------------------------------------
#? Game loop

def determine_winner(player_pick,cpu_pick): 
    # Each argument should be an int between 1 & 3
    # If player won, returns "player"
    # Vice-versa for "cpu"
    # Returns "draw" if values are equal
    p_pick = move_list[player_pick]
    c_pick = move_list[cpu_pick]

    if c_pick == p_pick:
        return "draw"
    elif p_pick["loses_to"] == cpu_pick: # The integer given
        return "cpu"
    elif c_pick["loses_to"] == player_pick: # The integer given
        return "player"
    

def cpu_pick():
    return randint(1,3)


def player_pick():
    clear()
    print("[!] Select a move:\n")
    print("[1]. Rock")
    print("[2]. Paper")
    print("[3]. Scissors\n")
    select = input("[?] ")
    return int(select)


def play_menu(player): #!WIP not functional yet
    while True:
        player = refresh_profile(player)
        clear()
        print("[!] Player: " + player["name"])
        print("[!] Balance: $" + str(player["balance"]))
        print("[!] Current bet: $" + str(player["bet"]))
        print("\n[1]. Throw!")
        print("[2]. Change your bet")
        print("[3]. See your stats")
        print("[4]. Return to menu")
        select = input("\n[?] ")
        if select == '1':
            play(player)
        elif select == '2':
            change_bet(player)
        elif select == "3":
            pass
        elif select == "4":
            return


def lose(player):
    # Find profile in JSON by name
    data = load_data()
    for prof in data["profiles"]:
        if prof["name"] == player["name"]:
            target_player = prof
    # Alter json profile values
    target_player["losses"] += 1
    target_player["balance"] -= player["bet"]
    if target_player["balance"] == 0:
        target_player["busts"] += 1

    save_data(data)
    

def win(player):
    # Find profile in JSON by name
    data = load_data()
    for prof in data["profiles"]:
        if prof["name"] == player["name"]:
            target_player = prof
    # Alter json profile values
    target_player["wins"] += 1
    target_player["balance"] += player["bet"]

    save_data(data)
    

def play(player):
    clear()
    player_choice = player_pick()
    cpu_choice = cpu_pick()
    print("\n[!] CPU is picking....")
    #sleep(2)
    winner = determine_winner(player_choice,cpu_choice)
    input("[!] Press enter to see the results.")
    clear()
    print(f"[!] {player['name']} picked " + move_list[player_choice]["move_name"])
    print(f"[!] CPU picked " + move_list[cpu_choice]["move_name"])
    if winner == 'player':
        print(f"\n[!] {player['name']} wins!")
        print(f"[!] ${str(player['bet'])} has been added to your balance")
        win(player)
        input("\n[!] Press enter to continue")
    elif winner == 'cpu':
        print("\n[!] CPU wins!")
        print(f"[!] ${str(player['bet'])} has been deducted from your balance")
        lose(player)
        input("\n[!] Press enter to continue")
    elif winner == 'draw':
        print("\n[!] Draw!")
        print("[!] Nothing lost, nothing gained.")
        input("[!] Press enter to continue")


#--------------------------------------------------------

def main():
    player = select_profile()
    while True:
        clear()
        print("\t#  Rock, Paper, Scissors  #\n")
        print("\n[!] Profile: " + player["name"] + '\n')
        print("[1]. Play")
        print("[2]. Manage profiles")
        print("[3]. Settings")
        print("[Q]. Exit")
        select = input("\n[?] ")
        if select.lower() == 'q':
            quit() 
        elif select == '1':
            play_menu(player) 
        elif select == '2':
            profile_management_menu() 
        elif select == '3':
            pass

try:
    main()
except KeyboardInterrupt:
    quit()

#--------------------------------------------------------
