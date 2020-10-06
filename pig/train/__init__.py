from itertools import product
from functools import partial
import numpy as np 
from numpy.random import rand 

from wasabi import msg, table, row
from tqdm import tqdm

def indexer(array): 
    imax, jmax, kmax = array.shape

    for i,j in reversed(list(zip(*np.triu_indices(imax)))):
        for k in range(100-i): 
            yield i,j,k 
        if i==j:
            continue
        for k in range(100-j): 
            yield j,i,k 


def training_loop(max_iter=100, tol=0.001): 
    P = rand(100, 100, 100)
    delta = 0 

    cache_indexes = list(indexer(P))

    print(row(data=('Iteration', 'Delta'), aligns=('c', 'c'), widths=(10, 10)))
    print("="*25)
    for iter_count in range(max_iter): 
                
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
            delta = 0 
            for i, j, k in cache_indexes: # indexer ensures we only loop over non winning states
                v = P[i,j,k]
                roll = 1 - P[j,i,0]         # rolled a 1. 
                
                for m in range(2,7): 
                    roll += P[i,j, k+m] if m < 100-i-k else 1   # reward only transition to winning states

                roll /= 6
                
                hold = 1 - P[j, i+k, 0] if i+k < 100 else 0

                P[i, j, k] = max(hold, roll) 
                delta = max(delta, np.abs(v-P[i,j,k]))
                
                t.postfix[1]["Delta"] = delta
                t.update(1)

            # delta = np.abs(v - P).max()

            if delta < tol:
                break

        print(row(data=(f"{iter_count+1}", f"{delta:.3f}"), aligns=('c', 'c'), widths=(10,10)))
    
    return P