import numpy as np

def linearize(numpyArray):
    return np.ravel(numpyArray)

def vectorized_result(v, h):
    e = np.zeros((2,1))
    e[0] = v
    e[1] = h
    return e
