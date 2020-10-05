from collections import defaultdict
from typing import ClassVar
from abc import ABC, abstractmethod

import attr 
from wasabi import msg

from .dice import Dice
from .constants import const


@attr.s(auto_attribs=True, repr=False)
class PlayerBase(ABC):
    action_dict:ClassVar = defaultdict(lambda: 'unknown', 
        {"H": "hold", "R": "roll"})

    name:str = None 
    score:int = 0
    turn_score:int = 0 
    dice:Dice = Dice.get_single_d6(seed=None)

    @abstractmethod
    def get_move(self, opponent): 
        """
        Override this method to implement movement aquisition logic
        """
        _turn_msg = f"Make your move {self}. "  \
                    + f"Your current score is {self.score} " \
                    + f"while your opponent's score is {opponent.score} " \
                    + "(R=roll, H=hold): "
        return _turn_msg
        
    def send(self, code): 
        if code in 'rhRH': 
            code = code.upper()
            action = self.action_dict[code]
        elif code in 'roll hold'.split():
            action = code 
        elif code in 'xX': 
            return const.EXIT
        
        effect = getattr(self, action, None) 
        
        if effect:
            signal = effect()
            msg.text(f"{self} score is {self.score}\n")
            return signal
        
        raise ValueError(f"Unhandled action: {action}. Valid actions are 'roll' or 'hold'")

    def roll(self):
        result = self.dice()
        
        if result == 1: 
            msg.warn(f"{self} has lost all points! 😭")
            return const.END_TURN

        self.turn_score += result
        
        msg.text(f"{self} total for this turn is {self.turn_score}")

        return const.CONTINUE

    def hold(self):
        msg.text(f"{self} has held. Adding turn score of {self.turn_score} to score.")

        self.score += self.turn_score
        return const.END_TURN 

    def reset_turn_score(self):
        self.turn_score = 0

    def __repr__(self): 
        return f"{self.name}"