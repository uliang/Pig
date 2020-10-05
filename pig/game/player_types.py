__all__=['Player', 'Npc']

from collections import defaultdict
from typing import ClassVar

import attr 
from wasabi import msg

from .dice import Dice
from .constants import const
from .base_classes import PlayerBase


class Player(PlayerBase): 
    @classmethod
    def from_input(cls): 
        for i in range(1, 3): 
            name = input(f"Player {i} name (Press Enter to accept default): ")
            msg.text( f"Player {i} {name} created" )

            yield cls(name) if name else cls(f"P{i}")

    def get_move(self, opponent):
        turn_msg = super().get_move(opponent)
        choice = input(turn_msg)
        return choice


@attr.s(repr=False)
class Npc(PlayerBase): 
    policy = attr.ib(default=None) 

    def __attrs_post_init__(self): 
        i = 2
        msg.text(f"Your challenger is {self.name} 🐷!")
        msg.text( f"Player {i} {self.name} created" )

    def get_move(self, opponent): 
        i, j, k = self.score, opponent.score, self.turn_score

        move = self.policy(i,j,k)

        turn_msg = "{} {}".format(super().get_move(opponent), move)
        msg.info(turn_msg)
        
        return move 

    