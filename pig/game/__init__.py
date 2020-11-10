from enum import Enum
from itertools import cycle
from random import randrange
from collections import namedtuple

from wasabi import msg

from .ai_wrapper import open_policy
from .constants import const

Player = namedtuple('Player', ['name', 'decision_function'])

def create_player(i, decision_function=None):

    msg.text(f"Player {i} name (Press <Enter> to accept default): ")

    if decision_function:
        p_name = "PigMachine"
    else:
        p_name = input()
        p_name = p_name if p_name else f"P{i}"
   
    return Player(p_name, decision_function)
    
def game_loop(num_players, ai_file=None):
    p1 = create_player(1)

    if num_players == 1:
        with open_policy(ai_file) as policy:
            p2 = create_player(2, policy)
    else:
        p2 = create_player(2) 
   
    player_sequence = [p1, p2] if randrange(2) else [p2, p1]

    msg.text(f"{player_sequence[0].name} goes first.")

    game = [0,0,0]
    state= None
    player, opp = player_sequence
    while 1:
        while 1:
            msg.text(f"{player.name} total score is {game[0]} and current round total is {game[2]}. "
                     + f"\n{opp.name} score is {game[1]}")

            if player.decision_function is None:
                msg.text(f"{player.name}, please choose your move (R to roll or H to hold): ")
                move = input()
            else:
                move = player.decision_function(*game)

            if move in ('r', 'R', 'roll'):
                roll=randrange(1,7)
                if roll > 1:
                    msg.text(f"{player.name} rolled a {roll}. {player.name} current round total "
                             + f"is {roll + game[2]}")
                    game[2] += roll
                else:
                    msg.text(f"{player.name} rolled a {roll} and lost all his points!")
                    break
            elif move in ('h', 'H', 'hold'):
                msg.text(f"{player.name} held. Adding {game[2]} to {game[0]} for "
                         + f"{player.name} total of {game[0]+game[2]}.")
                game[0] += game[2]
                break 
            elif move in ('x', 'X', 'q', 'Q', 'quit', 'end'):
                state = const.EXIT
                break

        if state is const.EXIT:
            msg.text("Exiting...")
            break

        if game[0] >= 100:
            msg.good(f"{player.name} wins!")
            break

        game[0], game[1], game[2] = game[1], game[0], 0
        player, opp = opp, player
    
