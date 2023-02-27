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
    while conf.lower() != "y" or conf.lower() != "n":
        conf = input("\n[?] Confirm? (Y/N) ")
    if conf.lower() == 'y':
        profile = {
            profile_name: {
            "balance":start_bal,
            "wins":0,
            "losses":0,
            "busts":0
        }}
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
        if conf.lower() != "y" or conf.lower() != "n":
            conf = input("\n[?] Create one now? (Y/N) ")
        if conf.lower() == 'y':
            create_profile()
            return
        elif conf.lower() == 'n':
            return 
    for name in profile_list:
        print(f"[{str(profile_list.index(name) + 1)}]. {name}")
    select = input("[?] ")
    return profile_list[int(select) - 1]




#--------------------------------------------------------
#? Game loop

#! I don't think this shit will work
#? Shit is skuffed but I think I made it work
def determine_winner(player_pick,cpu_pick): 
    # Each argument should be an int between 1 & 3
    # If player won, returns "player"
    # Vice-versa for "cpu"
    p_pick = move_list(player_pick)
    c_pick = move_list(cpu_pick)
    if p_pick["loses_to"] == cpu_pick: # The integer given
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
    #! Need to check input
    return int(select)


def play_menu(player):
    while True:
        clear()
        print("[!] Player: ")
        print("[!] Balance: ")
        print("\n[1]. Throw!")
        print("[2]. Return to menu")
        select = input("\n[?] ")
        if select == '1':
            pass 
        elif select == '2':
            return 


def play(player):
    clear()
    player_choice = player_pick()
    cpu_choice = cpu_pick()
    print("[!] CPU is picking....")
    #sleep(2)
    winner = determine_winner(player_choice,cpu_choice)
    input("[!] Press enter to see the results.")
    clear()
    # LEAVING OFF HERE




 
#--------------------------------------------------------

def main():
    while True:
        clear()
        print("\t#  Rock, Paper, Scissors  #\n")
        print("[1]. Play")
        print("[2]. Manage profiles")
        print("[3]. Settings")
        print("[Q]. Exit")
        select = input("\n[?] ")
        if select.lower() == 'q':
            quit() 
        elif select == '1':
            pass 
        elif select == '2':
            pass 
        elif select == '3':
            pass

try:
    main()
except KeyboardInterrupt:
    quit()

#--------------------------------------------------------
