from itertools import product
from functools import partial
import numpy as np 
from numpy.random import rand 

from tqdm import tqdm

def indexer(size): 

    for i,j in zip(*(reversed(id_arr) 
                    for id_arr in np.triu_indices(size))):
        yield i,j 

def training_loop(max_iter=10, tol=0.001): 
    P = rand(100, 100, 100)

    score_partition = list(indexer(100))
            
    bar_fmt = '{elapsed}|{bar}|{percentage:.0f}% [{rate_fmt}]'
    with tqdm(total=len(score_partition), ncols=60, unit_scale=1, 
              bar_format=bar_fmt, leave=False) as t:
        """
        The estimated value for each action is:
        'hold' = V(s'), 
        'roll' = \sum_s' 1/6 * ( R_ss' + V(s')) where the reward for holding
        is always 0 since you can never transition from a non-winning state
        to a winning state by holding. 

        R_ss' = 1 iff s -> s' is a transition from nonwinning to winning.
        """ 
        for I, J in score_partition:   
            delta = 0 
            for _ in range(max_iter): 
                i,j = I,J
                switched = 0 

                while switched < 2: 
                    for k in range(100-i): 
                        v = P[i,j,k]

                        roll = 1 - P[j,i,0]                             # rolled a 1. 
                        
                        for m in range(2,7): 
                            roll += P[i,j, k+m] if m < 100-i-k else 1   # reward only transition to winning states

                        roll /= 6
                        
                        hold = 1 - P[j, i+k, 0] if i+k < 100 else 0     # So that the AI learns to hold in a 
                                                                        # nonwinning state
                        P[i, j, k] = max(hold, roll) 
                    
                        delta = max(np.abs(v-P[i,j,k]), delta)

                    if i != j:
                        i,j = J,I
                        switched += 1 
                    else:
                        break 

                if delta < tol:
                    break
            
            t.update(1)

    return P
