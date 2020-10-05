__all__ = ['Dice']

import random 
import attr 


@attr.s(auto_attribs=True, repr=False)
class Dice:
    """
    Dice object 

    >>> dice = Dice.get_single_d6()
    >>> dice
    1D6
    >>> dice()
    1D6 Rolled: 6
    6
    """
    n_dice:int 
    sides:int 
    seed:int = 42
    modifier:int = 0

    @classmethod
    def get_single_d6(cls, seed=42):
        return cls(1, 6, seed=seed) 

    def __attrs_post_init__(self): 
        self._rand = random.Random(self.seed)

    def __repr__(self): 
        if self.modifier: 
            return f"{self.n_dice}D{self.sides}+{self.modifier}"
        return f"{self.n_dice}D{self.sides}" 

    def __str__(self): 
        return repr(self)

    def __call__(self): 
        die = list(range(1, self.sides+1))
        outcomes = [self._rand.choice(die) for _ in range(self.n_dice)]
        
        print(f"{self} Rolled:", *outcomes, sep=' ')
        
        return sum(outcomes) + self.modifier