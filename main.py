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
            "bet":10,
            "wins":0,
            "losses":0,
            "draws":0,
            "total_games":0,
            "gain":0,
            "busts":0
        }
        data["profiles"].append(profile)
        save_data(data)
        print(f"\n[!] Profile for {profile_name} saved.")
        input("[!] Press enter to continue.")
        return profile
    elif conf.lower() == 'n':
        print("\n[X] Profile skipped.")
        input("[!] Press enter to continue.")
        return


def select_profile():
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
            return create_profile()
        elif conf.lower() == 'n':
            return 
    clear()
    print("[!] Select a profile from the list")
    # Display numbered list for user to pick from
    # User input as the index value from profile_list
    for name in profile_list:
        print(f"[{str(profile_list.index(name) + 1)}]. {name['name']}")
    print()
    while True:
        select = input("[?] ")
        try:
            return profile_list[int(select) - 1]
        except:
            print("[X] Not valid.")
            pass


def refresh_profile(player):
    # Find "player" in JSON, return player dict
    # Used when changing JSON values during runtime
    data = load_data()
    for profile in data["profiles"]:
        if profile["name"] == player["name"]:
            return profile
    return select_profile()
    

def change_bet(player): 
    data = load_data()
    for prof in data["profiles"]:
        if prof["name"] == player["name"]:
            profile = prof
    clear()
    print("[!] Changing bet\n")
    print("[!] Current bet: $" + str(profile['bet']))
    print("[!] Current balance: $" + str(profile['balance']))
    while True:
        try:
            new_bet = int(input("\n[?] New bet: $")) 
            while new_bet > profile['balance']:
                print("\n[X] Too broke for that.")
                new_bet = int(input("\n[?] New bet: $"))
                break
            break
        except ValueError:
            print("[X] Bet must be a whole number")
    profile["bet"] = new_bet
    save_data(data)


def view_stats(player):
    clear()
    print("\t///  Statistics  ///\n")
    print("[~] Name: " + player['name'])
    print("[~] Balance: $" + str(player['balance']))
    print("[~] Total gain: $" + str(player['gain']))
    print("[~] Total busts: " + str(player['busts']))
    print()
    print("[~] Total games: " + str(player["total_games"]))
    print("[~] Total wins: " + str(player['wins']))
    print("[~] Total losses: " + str(player['losses']))
    print("[~] Total draws: " + str(player["draws"]))
    print()
    print("[~] Win/loss ratio: " + str(player['wins'] / player['losses']))
    input("\n[~] Press enter to continue ")


def profile_management_menu():
    while True:
        clear()
        print("[1]. View profiles")
        print("[2]. Add profiles")
        print("[3]. Delete profiles")
        print("[4]. Return to menu")
        select = input("\n[?] ")
        if select == '1':
            view_profiles()
        elif select == '2':
            create_profile()
        elif select == '3':
            delete_profile()
        elif select == '4':
            return


def view_profiles():
    data = load_data()
    profiles = data["profiles"]
    clear()
    for p in profiles:
        print("~ Name:  " + p["name"])
        print("~ Balance: $" + str(p["balance"]))
        print("~ Games: " + str(p["wins"] + p["losses"]))
        print()
    input("[~] Press enter to continue. ")


def delete_profile():
    clear()
    print("[X] ENTERED DELETE PROFILE MENU")
    print("[!] Changes cannot be reversed!")
    print("[~] Confirm?")
    conf = input("\n(Y/N) ")
    while conf.lower() != 'y' and conf.lower() != 'n':
        conf = input("\n(Y/N) ")
    if conf.lower() == 'n':
        return
    elif conf.lower() == 'y':
        prof = select_profile()
        data = load_data()
        i = data["profiles"].index(prof)
        data["profiles"].pop(i)
        save_data(data)
        print("\n[!] Profile deleted! ")
        input("[~] Press enter to continue. ")

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
    options = [1,2,3]
    clear()
    print("[!] Select a move:\n")
    print("[1]. Rock")
    print("[2]. Paper")
    print("[3]. Scissors\n")
    while True:
        try:
            select = int(input("[?] "))
            while select not in options:
                print("[X] Selection must be a number between 1 and 3.")
                select = int(input("[?] "))
            break
        except ValueError:
            print("[X] Error: Bad value")
            print("[X] Selection must be a number between 1 and 3.")
    return select


def bust(player):
    clear()
    data = load_data()
    for profile in data["profiles"]:
        if profile["name"] == player["name"]:
            profile["busts"] += 1
            profile["balance"] += 100
    save_data(data)
    print("[!] YOU BUSTED!")
    print("[!] Your account has reached $0 :(")
    print("\n[~] However, since this is just a game, $100 will be")
    print("    added to your account. But, your \"busts\" statistic")
    print("    will go up by one, as a reminder to your poor money")
    print("    management skills. ")
    input("\n[~] Press enter to continue. ")


def play_menu(player): 
    while True:
        player = refresh_profile(player)
        if player["balance"] == 0:
            bust(player)
            return
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
            if player["bet"] > player["balance"]:
                clear()
                print("[X] You don't have enough to cover this bet!")
                print("[X] Change your bet to something you can afford.")
                input("\n[!] Press enter to continue.")
            else:
                play(player)
        elif select == '2':
            change_bet(player)
        elif select == "3":
            view_stats(player)
        elif select == "4":
            return


def lose(player):
    # Find profile in JSON by name
    data = load_data()
    for prof in data["profiles"]:
        if prof["name"] == player["name"]:
            target_player = prof
    # Alter json profile values
    target_player["total_games"] += 1
    target_player["losses"] += 1
    target_player["balance"] -= player["bet"]
    target_player["gain"] -= player['bet']
    # if target_player["balance"] == 0:
    #     target_player["busts"] += 1
    save_data(data)
    

def win(player):
    # Find profile in JSON by name
    data = load_data()
    for prof in data["profiles"]:
        if prof["name"] == player["name"]:
            target_player = prof
    # Alter json profile values
    target_player["total_games"] += 1
    target_player["wins"] += 1
    target_player["balance"] += player["bet"]
    target_player['gain'] += player['bet']
    save_data(data)
    

def draw(player):
    # Find profile in JSON by name
    data = load_data()
    for prof in data["profiles"]:
        if prof["name"] == player["name"]:
            target_player = prof
    target_player["total_games"] += 1
    target_player["draws"] += 1
    save_data(data)


def play(player):
    clear()
    player_choice = player_pick()
    cpu_choice = cpu_pick()
    print("\n[!] CPU is picking....")
    #sleep(2)
    # Returns string, either "player","cpu", or "draw"
    winner = determine_winner(player_choice,cpu_choice)
    input("[!] Press enter to see the results.")
    clear()
    print(f"[!] {player['name']} picked " + move_list[player_choice]["move_name"])
    print(f"[!] CPU picked " + move_list[cpu_choice]["move_name"])
    # Player wins
    if winner == 'player':
        print(f"\n[!] {player['name']} wins!")
        print(f"[!] ${str(player['bet'])} has been added to your balance")
        win(player)
        input("\n[!] Press enter to continue")
    # CPU wins
    elif winner == 'cpu':
        print("\n[!] CPU wins!")
        print(f"[!] ${str(player['bet'])} has been deducted from your balance")
        lose(player)
        input("\n[!] Press enter to continue")
    # Draw, same selection
    elif winner == 'draw':
        print("\n[!] Draw!")
        print("[!] Nothing lost, nothing gained.")
        draw(player)
        input("[!] Press enter to continue")

#--------------------------------------------------------
#? Settings

def change_start_bal(): #!
    data = load_data()
    current_bal = data["settings"]["start_bal"]
    clear()
    print("[!] Changing starting balance.")
    print("[!] Current value: $" + str(current_bal))
    print()
    while True:
        try:
            new_bal = int(input("[?] New value: $"))
            break
        except ValueError:
            print("[X] Value must be a whole number.")
    data["settings"]["start_bal"] = new_bal
    save_data(data)
    print("\n[!] Settings updated")
    input("[~] Press enter to continue ")
    

def toggle_throw_pause():
    data = load_data()
    tp_value = data["settings"]["throw_pause"]
    data["settings"]["throw_pause"] = not tp_value
    save_data(data)


def delete_profile_data():
    clear()
    print("[X] YOU ARE ABOUT TO DELETE ALL PROFILES")
    print("[!] Are you sure you want to continue?")
    conf = input("\n(Y/N) ")
    while conf.lower() != 'y' and conf.lower() != 'n':
        conf = input("(Y/N) ")
    if conf.lower() == 'y':
        data = load_data()
        data["profiles"] = []
        save_data(data)
        print("\n[!] Save data has been deleted.")
        input("[~] Press enter to continue. ")
    elif conf.lower() == 'n':
        print("\n[!] Cancelled")
        input("[~] Press enter to continue. ")        


def settings_menu():
    while True:
        data = load_data()
        start_bal = data["settings"]["start_bal"]
        if data["settings"]["throw_pause"]:
            tp_state = 'ON'
        else:
            tp_state = 'OFF'
        clear()
        print("\t///  Settings  ///")
        print(f"[1]. Change starting balance (${str(start_bal)})")
        print(f"[2]. Toggle Throw Pause ({tp_state})")
        print("[3]. Delete profile data")
        print("[4]. Return to menu")
        select = input("\n[?] ")
        if select == '1':
            change_start_bal()
        elif select == '2':
            toggle_throw_pause()
        elif select == '3':
            delete_profile_data()
        elif select == '4':
            return

#--------------------------------------------------------

def main():
    player = select_profile()
    while True:
        player = refresh_profile(player)
        clear()
        print(player)
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
            settings_menu()

try:
    main()
except KeyboardInterrupt:
    quit()

#--------------------------------------------------------
