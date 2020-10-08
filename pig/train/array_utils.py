import numpy as np

def set_ones(width, ones_start=0, ones_stop=0):
    """
    set_ones creates row vectors of the form 
        v=[0,...,0,1,..........,1,0,...,0]
              ones_start  ones_stop
    If ones_start is larger than or equal to width, return vector of 
    zeros. 
    >>> set_ones(6, 7, 10)
    array([0., 0., 0., 0., 0., 0.])
    >>> set_ones(6, 1, 3)
    array([0., 1., 1., 0., 0., 0.])
    """
    v = np.zeros(width)
    if ones_start < width:
        v[ones_start:ones_stop] = 1
    return v 

def set_b(width):
    """
    set_b creates a vector of ones that terminates with the
    sequence 2,3,4,5,6,6. 
    >>> set_b(10)
    array([1., 1., 1., 1., 2., 3., 4., 5., 6., 6.])
    >>> set_b(1)
    array([6.])
    >>> set_b(2)
    array([6., 6.])
    >>> set_b(3)
    array([5., 6., 6.])
    >>> set_b(4)
    array([4., 5., 6., 6.])
    >>> set_b(8)
    array([1., 1., 2., 3., 4., 5., 6., 6.])
    """
    b = np.ones(width)
    b[-1] = 6 
    boundary = max(2, 8-width)
    seq = np.arange(boundary, 7)
    b[-1-len(seq):-1] = seq   
    return b
