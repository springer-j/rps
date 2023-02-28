# rps
Rock, Paper, Scissors

Nothing crazy, just goofing off.
Not finished if you were thinking about running anything.

              ///  History  ///

[2/26/23] Initial upload, unfinished, doesn't run

[2/27/23] Added functions, fixed issues. Works but buggy.



---------------------------------------------------------------------------------

Title: 		# RPS Project Notes
Date:  		# 2/25/23 
System:		# Icebox

---------------------------------------------------------------------------------

- How does the balance system work? Is there a set bet?
  cost to play? How much? User decided? Does user have enough 
  money to throw again? 

- Profile value in json is messed up. Profiles are a dict... inside of a 
  dict... inside of a list. wtf.

- FORGOT THAT DRAWS CAN HAPPEN
- How am I gonna select the program from the JSON with the one loaded in the 
  program?
  - if player["name"] == json_profile["name"] ?
  - Have to make sure there's no duplicate names
    - More input validation ugh
---------------------------------------------------------------------------------

                    ///  To-Do  ////

[X] Overhaul profile creation and json format

[X] Select profile

[X] Add "draw" outcome

[X] Win/lose functions
    - Adjust player balance
    - Adjust player w/l counts
    - Update json
    - Check if player bal <= 0
    - Will have to refresh profile values
[X] Fix determine_winner system 

[X] Game loop/play functions

[X] Integrate balance system

[X] Add "change bet" functionality
    - Can't bet more than in balance


[0] Move select_profile from boot to after selecting "Play"

[0] "My stats" display

[0] View Profiles

[0] Remove profiles

[0] A LOT of input validation

---------------------------------------------------------------------------------
