from enum import Enum
from itertools import cycle

import plac
from wasabi import msg

from .dice import * 
from .player_types import *
from .constants import const


def game_loop(p1:Player, p2:Player):
    
    for player, opponent in cycle([(p1, p2), (p2, p1)]): 
        player.reset_turn_score() 
        
        signal = const.CONTINUE
        
        while signal is const.CONTINUE: 

            move = player.get_move(opponent)
            try: 
                signal = player.send(move)
            except ValueError:
                continue
            
            if signal is const.END_TURN:
                msg.text(f"{player} has ended his turn\n")
                break
            elif signal is const.EXIT:
                msg.info("Exiting")
                return 0


        if player.has_won:
            break 
    
    msg.good(f"{player} wins!")