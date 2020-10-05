__all__=['Player', 'Npc']

from collections import defaultdict
from typing import ClassVar

import attr 
from wasabi import msg

from .dice import Dice
from .constants import states
from .base_classes import PlayerBase


class Player(PlayerBase): 
    def get_move(self, opponent):
        turn_msg = super().get_move(opponent)
        choice = input(turn_msg)
        return choice


@attr.s
class Npc(PlayerBase): 
    _policy = attr.ib() 

    def get_move(self, opponent): 
        pass 

    