from enum import Enum 


class states(Enum): 
    END_TURN    = 0
    CONTINUE    = 1
    EXIT        = 2
    NPC         = 3
    PC          = 4