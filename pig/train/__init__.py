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
        (99,99), 
        (98,99), 
        (97,99), (98,98), 
        (96,99), (97,98), ...
        ...
        (0, 99), ..., (49, 50)
        (0, 98), ..., (49, 49)
        ...
        (0, 0)
    """
    for s_part in range(198, -1, -1):
        for i in range(max(0,s_part-99), math.ceil((s_part+1)/2)):
            yield i, s_part-i 

def training_loop(max_iter=10, tol=0.001): 
    """
    training_loop performs value iteration for the Pig game. 
    """ 
    P = rand(100, 100, 100)

    score_partition = list(indexer(100))
            
    bar_fmt = '{elapsed}|{bar}|{percentage:.0f}% [{rate_fmt}]'
    with tqdm(total=len(score_partition), ncols=60, unit_scale=1, 
              bar_format=bar_fmt, leave=False) as t:
        for i, j in score_partition:   
            for _ in range(max_iter):
                v = np.r_['c', P[i, j, 0:100-i], P[j, i, 0:100-j]]
                
                b_ = np.r_['c', set_b(100-i), set_b(100-j)]

                hold = np.r_['c', [1-P[j, _i, 0] for _i in range(i,100)], 
                                  [1-P[i, _j, 0] for _j in range(j,100)]]

                A = np.c_[[set_ones(100-i, k+2, k+7) for k in range(100-i)]]
                B = np.c_[[-1*set_ones(100-j, 0, 1) for k in range(100-i)]]
                C = np.c_[[-1*set_ones(100-i, 0, 1) for k in range(100-j)]]
                D = np.c_[[set_ones(100-j, k+2, k+7) for k in range(100-j)]] 

                M = np.matrix(np.r_[np.c_[A, B], np.c_[C, D]])

                v_temp = np.maximum((M @ v + b_)/6, hold)
                
                P[i, j, 0:100-i] = v_temp[0:100-i, 0].T
                P[j, i, 0:100-j] = v_temp[100-i:, 0].T

                delta = np.abs(v-v_temp).max()

                if delta < tol:
                    break
            
            t.update(1)

    return P
