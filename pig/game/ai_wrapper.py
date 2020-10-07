from contextlib import contextmanager 
from functools import partial
import pkg_resources
import attr

import numpy as np
import h5py 

    
def policy_func(P, i, j, k):
    if i + k >= 100:
        return 'hold' 
    
    actions = [
        (1-P[j, i+k, 0], 'hold'),
        ( (P[i,j,k+2:k+7].sum() + 1-P[j,i,0])/6, 'roll' )
    ]
    return max(actions)[1]


@contextmanager
def open_policy(ai_file): 
    if ai_file is None: 
        ai_file = pkg_resources.resource_filename('pig', 'game/pig_ai.hdf5')
    pfile = h5py.File(ai_file, 'r')
    policy_dset = pfile['policy']
    
    P = np.zeros((100, 100, 100))
    policy_dset.read_direct(P)
    
    policy = partial(policy_func, P)

    try:
        yield policy
    finally:
        pfile.close()
