from itertools import product
from functools import partial
import numpy as np 
from numpy.random import rand 

from wasabi import msg
from tqdm import tqdm

def iswin(i,j,k): 
    return i+k >= 100

def indexer(array): 
    imax, jmax, kmax = array.shape

    for i,j in reversed(list(zip(*np.triu_indices(imax)))):
        for k in range(100-i): 
            yield i,j,k 
        if i==j:
            continue
        for k in range(100-j): 
            yield j,i,k 

def reward(old_state, new_state): 
    """
    Set reward to be 1 if old_state is a nonwinning state 
    and new_state is a winning state and 0 for all other 
    transitions. 
    """
    if not iswin(*old_state) and iswin(*new_state):
        return 1 
    return 0 

def value(P, i,j,k): 
    """
    For Pig, the value of a state is 
    the probability of winning the game from a nonwinning state 
    and 0 otherwise. 
    """
    if iswin(i,j,k):
        return 0
    return P[i,j,k]

def init_policy(array): 
    a = np.array(array)
    
    with np.nditer(a, order='K', 
                   flags=['multi_index'], op_flags=['readwrite']) as it: 
        for x in it: 
            x[...]=1 if iswin(*it.multi_index) else x
    
    return a 

def training_loop(max_iter=100, tol=0.001): 
    P = np.ones((100, 100, 100)) 
    delta = 0 

    # P = init_policy(P)
    V = partial(value, P)
    cache_indexes = list(indexer(P))

    for _ in range(max_iter): 
        
        v = np.array(P)
        
        for i, j, k in tqdm(cache_indexes, ncols=80, 
                            bar_format='{elapsed}|{bar}|{percentage:.0f}% [{rate_fmt}]'):
            """
            The estimated value for each action is:
            'hold' = V(s'), 
            'roll' = \sum_s' 1/6 * ( R_ss' + V(s')) where the reward for holding
            is always 0 since you can never transition from a non-winning state
            to a winning state by holding. 

            R_ss' = 1 iff s -> s' is a transition from nonwinning to winning.
            """ 
            roll = (1/6)*(
                reward((i, j, k), (i, j, 0)) + V(i, j, 0)
                + sum(reward((i, j, k), (i, j, k+m)) + V(i, j, k+m)
                    for m in range(2,7))
            )  
            hold = V(i+k, j, 0)

            P[i, j, k] = max(hold, roll) 

        delta = np.abs(v - P).max()
        msg.text(f"Delta: {delta:.4f}")

        if delta < tol:
            break
    
    return P