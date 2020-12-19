"""
File:         pyopoly.py
Author:       Vu Nguyen
Date:         10/31/2020
Section:      31
E-mail:       vnguye12@umbc.edu
Description:  This is a superior version of the actual monopoly games.
              Only intelligent people can play this. First, each
              player enters in their name and chooses their symbol (a single
              capital letter). Then the game will start immediately.
              During the player's turn, they have the options to choose
              what they want to do during their. The game is over once
              one of the player ran out of money.
"""

from sys import argv
from random import randint, seed
from board_methods import load_map, display_board

# possibly a lot more code here.
# this code can be anywhere from right under the imports to right # above if __name__ == '__main__':
if len(argv) >= 2:
    seed(argv[1])

# Constants
STARTING_MONEY = 1500
PASS_GO_MONEY = 200
NUMBER_OF_PLAYER = 2
PLAYER_ONE = 1
STARTING_POSITION = 0
CANT_BUY = -1
BOARD_FILE = 'proj1_board1.csv'
SYMBOL = "Symbol"
MONEY = "Money"
POSITION = "Position"
TURN = "Turn"
PLACE = 'Place'
Abbrev = 'Abbrev'
PRICE = 'Price'
RENT = 'Rent'
BUILDING_RENT = 'BuildingRent'
BUILDING_COST = 'BuildingCost'
PROPERTIES = 'Properties'
LOSE = 'Lose'


# This is the official starting function.
def play_game(pass_go_money, board_file, players_stat):

    place_info = load_map(board_file)

    # This loop turn all of the string price, rent, and building rent into integer
    for places in place_info:
        places[PRICE] = int(places[PRICE])
        places[RENT] = int(places[RENT])
        places[BUILDING_RENT] = int(places[BUILDING_RENT])
        places[BUILDING_COST] = int(places[BUILDING_COST])

    # This loop set up the board with abbreviate name
    the_board = []
    for line in load_map(board_file):
        the_board.append(line["Abbrev"].ljust(5) + '\n     ')

    # Each player take their turn inside this while loop, only when they haven't lost all of their money yet.
    game_over = False
    while not game_over:

        # Rolling the dice and setting up the player position an switching player turns for the next roll.
        dice_move = randint(1, 6) + randint(1, 6)
        take_turn(dice_move, players_stat)

        # This loop/condition check which player is in play.
        for player in players_stat:
            if not players_stat[player][TURN]:

                # Display the player's position on the board
                format_display(the_board, players_stat, player)
                print(player, ", you'd rolled", dice_move)

                # This loop go through all the map position and checked which property matched the player's position
                for line in place_info:
                    board_position = players_stat[player][POSITION] % len(the_board)

                    # This condition tells me which place the players landed on
                    if board_position == int(line[POSITION]):
                        print(player, "you'd landed on", line[PLACE])

                        # This condition check if the player pass go
                        if players_stat[player][POSITION] >= len(the_board):
                            players_stat[player][POSITION] -= len(the_board)
                            players_stat[player][MONEY] += pass_go_money
                            print('You landed or passed go, $200 dollar added to your balance.')

                            rent_calculator(player, players_stat, line)
                        else:
                            rent_calculator(player, players_stat, line)

                        # This condition make sure that the player haven't lost yet.
                        if not players_stat[player][LOSE]:

                            # This loop cycle through all the choices player can choose from.
                            turn_over = False
                            while not turn_over:

                                print('\n\t1. Buy Property\n'
                                      '\t2. Get Property Info\n'
                                      '\t3. Get Player Info\n'
                                      '\t4. Build a Building\n'
                                      '\t5. End Turn\n')

                                user_input = input('What do you want to do? \n')

                                # This condition checks for bad choices
                                if user_input.lower() in ['1', 'buy property']:
                                    buy_property(players_stat, line, place_info)

                                elif user_input.lower() in ['2', 'get property info']:
                                    get_property_info(players_stat, place_info)

                                elif user_input.lower() in ['3', 'get player info']:
                                    get_player_info(players_stat, place_info)

                                elif user_input.lower() in ['4', 'build a building']:
                                    build_a_building(players_stat, place_info)

                                elif user_input.lower() in ['5', 'end turn']:
                                    print('End Turn')
                                    turn_over = True

                                else:
                                    print('Invalid Input, try again!')

                        else:
                            game_over = True

    winner = ''
    loser = ''
    # This loop assign the winner and the loser.
    for players in players_stat:
        if players_stat[players][LOSE]:
            loser = players
        else:
            winner = players

    print(loser, 'you\'ve ran out of money.', winner, 'WIN!')


# This function set position of a player and modify their turn
def take_turn(move, players_stat):

    # This loop switches the players turn from True to False and update their position.
    for player in players_stat:
        if players_stat[player][TURN]:
            players_stat[player][POSITION] += move
            players_stat[player][TURN] = False
        else:
            players_stat[player][TURN] = True


# This function display the current position of the players
def format_display(board, players_stat, current_player):

    copy_board = list(board)

    # This loop/condition checks for other players (who is not in played)
    for player in players_stat:
        if players_stat[player][TURN]:

            cur_player_pos = players_stat[current_player][POSITION] % len(board)
            other_player_pos = players_stat[player][POSITION] % len(board)

            # If two player are in the same position display both player side by side
            if players_stat[current_player][POSITION] == players_stat[player][POSITION]:
                copy_board[other_player_pos] = copy_board[other_player_pos][:6] + players_stat[player][SYMBOL]
                copy_board[other_player_pos] = copy_board[other_player_pos][:7] + players_stat[current_player][SYMBOL]
            else:
                copy_board[other_player_pos] = copy_board[other_player_pos][:6] + players_stat[player][SYMBOL]
                copy_board[cur_player_pos] = copy_board[cur_player_pos][:6] + players_stat[current_player][SYMBOL]

    display_board(copy_board)
    print()


# This function get the information of the two player and store it in the players_info
def setting_up_player_info(start_money):

    player_dict = {}

    # This loop add player to the dictionary
    for num in range(NUMBER_OF_PLAYER):
        player_name = input("Player " + str(num + 1) + ", what is your name? ").strip()
        player_symbol = input("Player " + str(num + 1) + ", what symbol do you want to use? ").strip()

        # This loop ensure that the symbol is a single capital letter
        while (len(player_symbol) != 1) or not (65 <= ord(str(player_symbol)) <= 90):
            player_symbol = input("Player " + str(num + 1) + ", what symbol do you want to use? ").strip()

        player_dict[player_name] = {SYMBOL: player_symbol, MONEY: start_money, POSITION: STARTING_POSITION,
                                    TURN: False, LOSE: False, PROPERTIES: []}

        # This condition let player 1 goes first
        if num + 1 == PLAYER_ONE:
            player_dict[player_name][TURN] = True

    return player_dict


# This function check if the player ran out of money.
def out_of_money(current_player, players_stat):
    if players_stat[current_player][MONEY] <= 0:
        players_stat[current_player][LOSE] = True


# This function calculate the rent and subtract it from the total amount of money (NOT FINISHED)
def rent_calculator(player, players_stat, place_info):
    other_player = ''
    current_player = player

    # This loop assign the other player [Next Turn].
    for person in players_stat:
        if players_stat[person][TURN]:
            other_player = person

    # Check to see if this property have rent and is owned by someone.
    if place_info[RENT] != CANT_BUY and place_info[PRICE] == CANT_BUY:

        # Check to see if the other player own the property or not.
        if place_info[PLACE] in players_stat[other_player][PROPERTIES]:
            print('You\'ve landed on', other_player, '\'s property, you must pay rent!')

            # This condition checks if the other person have building on their property or not.
            if place_info[BUILDING_COST] == CANT_BUY:
                players_stat[current_player][MONEY] -= place_info[BUILDING_RENT]
                players_stat[other_player][MONEY] += place_info[BUILDING_RENT]
                out_of_money(current_player, players_stat)
                print(current_player + ' you paid', place_info[BUILDING_RENT], 'in building rent. ' +
                      'Your new balance is: ', players_stat[current_player][MONEY])

            else:
                players_stat[current_player][MONEY] -= place_info[RENT]
                players_stat[other_player][MONEY] += place_info[RENT]
                out_of_money(current_player, players_stat)
                print(current_player + ' you paid', place_info[RENT], 'in property rent. ' +
                      'Your new balance is: ', players_stat[current_player][MONEY])


# This function buy property (Not Finished, Prevent over buying property that cost too much!)
def buy_property(players_stat, current_property, place_info):
    cant_be_bought = True

    for player in players_stat:

        # This condition checks to see if the property is available
        if current_property[PRICE] != CANT_BUY:

            # Check which players is in play
            if not players_stat[player][TURN]:

                # Check to see if that player have enough money.
                if players_stat[player][MONEY] > current_property[PRICE]:

                    # This condition check to see if the player want to buy the property he/she landed on.
                    user_answer = input('Property is unknown, do you wish to buy it? ').strip()
                    if user_answer.lower() in ['yes', 'y']:
                        players_stat[player][PROPERTIES].append(current_property[PLACE])
                        players_stat[player][MONEY] -= current_property[PRICE]
                        current_property[PRICE] = CANT_BUY
                        cant_be_bought = False
                        print('You\'ve successfully bought', current_property[PLACE])
                    else:
                        print('You have decided not to buy', current_property[PLACE])
                        cant_be_bought = False
                else:
                    print(player + ', you don\'t have enough money to buy', current_property[PLACE])
                    cant_be_bought = False
        else:
            if current_property[PLACE] in players_stat[player][PROPERTIES]:
                cant_be_bought = False
                print(player, 'is the owner of this property you can not buy it.')

    if cant_be_bought:
        print('You can not buy this property, it can not be bought or sold!')


# This function display property information (NOT FINISHED)
def get_property_info(players_stat, place_info):
    player_property = ''
    invalid_name = True
    property_name = input('Which property do you want to get the info? ').strip()

    # This loop through the entire board to retrieve the property info.
    for places in place_info:
        if property_name == places[PLACE]:
            invalid_name = False

            # Fix this print statement below 'Owner and Building'
            print('\n' + property_name, '\n'
                  'Price:', places[PRICE], '\n'
                  'Owner:', end=' ')

            # This condition checks who own the property
            for player in players_stat:
                if places[PLACE] in players_stat[player][PROPERTIES]:
                    player_property = player

            # This condition checks who own the property
            if player_property:
                print(player_property)
            else:
                print('BANK')

            print('Building: ', end='')

            # This condition check if someone build a building on it.
            if places[BUILDING_COST] == CANT_BUY:
                print('YES')
            else:
                print('NO')

            print('Rent:', places[RENT], ',', places[BUILDING_RENT], '(with building)')

    if invalid_name:
        get_property_info(players_stat, place_info)


# This function display player information
def get_player_info(players_stat, place_info):
    invalid_name = True

    # This loop displays the players
    print("The players are:")
    for player in players_stat:
        print('\t\t', player)

    # This loop display the chosen player info
    chosen_one = input("What player do you wish to know? ").strip()
    for player in players_stat:
        if chosen_one.lower() == player.lower():
            invalid_name = False

            # Fix this print statement below 'Properties Owned'
            print('\n\tName:', player, '\n'
                  '\tSymbol:', players_stat[player][SYMBOL], '\n'
                  '\tMoney:', players_stat[player][MONEY], '\n'
                  '\n\tProperties Owned:\n')

            # This loop display the properties info
            if not players_stat[player][PROPERTIES]:
                print("\t\t", player, "is currently doesn't own any properties.")
            else:

                # Print out all the property own by a player.
                for property_name in players_stat[player][PROPERTIES]:
                    print('\t\t', property_name, 'with a building: ', end='')

                    # Cycle through the entire property listed.
                    for line in place_info:
                        if line[PLACE] == property_name:
                            if line[BUILDING_COST] == CANT_BUY:
                                print('True')
                            else:
                                print('False')

    # This loop check for invalid name input
    if invalid_name:
        get_player_info(players_stat, place_info)


# Prevent buying property that cost too much.
def build_a_building(player_stat, place_info):
    fail_to_built = False

    # Loop and check to see who is in play.
    for player in player_stat:
        if not player_stat[player][TURN]:

            # Check if player have any property
            if player_stat[player][PROPERTIES]:

                # These loops display all available property that can have building on it.
                for places in player_stat[player][PROPERTIES]:
                    for line in place_info:
                        if line[PLACE] == places and line[BUILDING_COST] != CANT_BUY:
                            print(places, line[Abbrev], line[BUILDING_COST])

                # This loop check to see if there any property match with the property player want to build building on.
                buy_building = input('Which property do you want to build a building on? ').strip()
                for prop_name in place_info:
                    if buy_building == prop_name[PLACE] or buy_building == prop_name[Abbrev]:

                        # This condition make sure that the player have enough money to buy the building.
                        if player_stat[player][MONEY] > prop_name[BUILDING_COST]:
                            if prop_name[BUILDING_COST] != CANT_BUY:
                                print('You have built building for', prop_name[PLACE])
                                player_stat[player][MONEY] -= prop_name[BUILDING_COST]
                                prop_name[BUILDING_COST] = CANT_BUY
                            else:
                                fail_to_built = True
                        else:
                            print(player + ', you don\'t have enough money to build your building.')

                if fail_to_built:
                    print("The property either have a building, isn't yours, or doesn't exist.")
            else:
                print('You don\'t own any properties.')


if __name__ == "__main__":
    players_info = setting_up_player_info(STARTING_MONEY)
    play_game(PASS_GO_MONEY, BOARD_FILE, players_info)
