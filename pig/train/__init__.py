from itertools import product
from functools import partial
import numpy as np 
from numpy.random import rand 

from wasabi import msg, table, row
from tqdm import tqdm

def indexer(array): 
    imax, jmax, kmax = array.shape

    for i,j in zip(*(reversed(id_arr) 
                    for id_arr in np.triu_indices(imax))):
        for k in range(100-i-1, -1, -1): 
            yield i,j,k 
        if i==j:
            continue
        for k in range(100-j-1, -1, -1): 
            yield j,i,k 


def training_loop(max_iter=10, tol=0.001): 
    P = rand(100, 100, 100)

    cache_indexes = list(indexer(P))
            
    bar_fmt = '{elapsed}|{bar}|{percentage:.0f}% {postfix[0]}{postfix[1][Delta]:>6.4f} [{rate_fmt}]'
    with tqdm(total=len(cache_indexes), ncols=60, unit_scale=1, postfix=["Delta=", dict(Delta=0)], 
                bar_format=bar_fmt, leave=False) as t:
        """
        The estimated value for each action is:
        'hold' = V(s'), 
        'roll' = \sum_s' 1/6 * ( R_ss' + V(s')) where the reward for holding
        is always 0 since you can never transition from a non-winning state
        to a winning state by holding. 

        R_ss' = 1 iff s -> s' is a transition from nonwinning to winning.
        """ 
        # print(row(data=('State', 'Delta'), aligns=('c', 'c'), widths=(10, 10)))
        # print("="*25)
        for i, j, k in cache_indexes:   # indexer ensures we only loop over non winning states
            delta = 0 
            for iter_count in range(max_iter): 
                v = P[i,j,k]
                roll = 1 - P[j,i,0]         # rolled a 1. 
                
                for m in range(2,7): 
                    roll += P[i,j, k+m] if m < 100-i-k else 1   # reward only transition to winning states

                roll /= 6
                
                hold = 1 - P[j, i+k, 0] if i+k < 100 else 0     # So that the AI learns to hold in a 
                                                                # nonwinning state
                P[i, j, k] = max(hold, roll) 
                delta = max(delta, np.abs(v-P[i,j,k]))
                
                t.postfix[1]["Delta"] = delta

                if delta < tol:
                    break
            
            t.update(1)

            # print(row(data=(f"<{i},{j},{k}>", f"{P[i,j,k]:.3f}"), 
            #           aligns=('c', 'c'), widths=(10,10)))
    
    return P