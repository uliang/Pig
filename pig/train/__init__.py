import math
import numpy as np 
from numpy.random import rand 

from tqdm import tqdm

from .array_utils import set_ones, set_b 

def indexer(size): 
    """
    indexer ensures that indices of the array are partitioned and yielded
    according to their total scores. The intended sequence of index pairs
    are
        (99,99), (98,99), (97,99), (98,98), (96,99), (97,98), ...
    """
    for s_part in range(198,-1, -1):
        for i in range(s_part-99, math.ceil((s_part+1)/2)):
            yield i, s_part-i 

def training_loop(max_iter=10, tol=0.001): 
    """
    The estimated value for each action is:
    'hold' = V(s'), 
    'roll' = \sum_s' 1/6 * ( R_ss' + V(s')) where the reward for holding
    is always 0 since you can never transition from a non-winning state
    to a winning state by holding. 

    R_ss' = 1 iff s -> s' is a transition from nonwinning to winning.
    """ 
    P = rand(100, 100, 100)

    score_partition = list(indexer(100))
            
    bar_fmt = '{elapsed}|{bar}|{percentage:.0f}% [{rate_fmt}]'
    with tqdm(total=len(score_partition), ncols=60, unit_scale=1, 
              bar_format=bar_fmt, leave=False) as t:
       for i, j in score_partition:   
            delta = 0 

            v = np.r_[P[i, j, 0:100-i], P[j, i, 0:100-j]].T
            
            b = np.r_[set_b(100-i), set_b(100-j)].T

            hold = np.array([1-P[j, _i, 0] for _i in range(i,100)] 
                              + [1-P[i, _j, 0] for _j in range(j,100)]).T 

            A = np.c_[[set_ones(100-i, k+2, k+7) for k in range(100-i)]]
            B = np.c_[[-1*set_ones(100-j, 0, 1) for k in range(100-i)]]
            C = np.c_[[-1*set_ones(100-i, 0, 1) for k in range(100-j)]]
            D = np.c_[[set_ones(100-j, k+2, k+7) for k in range(100-j)]] 

            M = np.matrix(np.c_[np.r_[A, B], np.r_[C, D]])

            v_temp = np.maximum(M @ v + b, hold).T
            
            P[i, j, 0:100-i] = v_temp[0:100-i]
            P[j, i, 0:100-j] = v_temp[100-i:]

            delta = np.abs(v-v_temp).max()

            if delta < tol:
                break
        
            t.update(1)

    return P
