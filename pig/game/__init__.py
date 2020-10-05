from enum import Enum
from itertools import cycle

import plac
from wasabi import msg

from .dice import * 
from .player import *
from .constants import states


def game_loop(p1:Player, p2:Player):
    for player in cycle([p1, p2]): 
        player.reset_turn_score() 
        
        signal = states.CONTINUE
        
        while signal is states.CONTINUE: 

            choice = input(
                f"Make your move {player}." + 
                f"Your current score is {player.score} (R=roll, H=hold): ")
            try: 
                signal = player.send(choice)
            except ValueError:
                continue
            
            if signal is states.END_TURN:
                msg.text(f"{player} has ended his turn\n")
                break
            elif signal is states.EXIT:
                msg.info("Exiting")
                return 0


        if player.score >= 100:
            break 
    
    msg.good(f"{player} wins!")