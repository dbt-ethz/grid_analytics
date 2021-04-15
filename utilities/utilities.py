import numpy as np


__all__ = ['array_move']


def array_move(array, vec):
    """ move the solid cells in the array based on a give vector

    Parameters
    ----------
    array: numpy ndarray
        numpy array with values of 0 and 1. 0 represents void cell and 1 represents solid.
    vec: a list or tuple of 3 float
    
    Returns
    -------
    numpy ndarray
    """
    for i in range(3):
        array = np.roll(array, vec[i], axis=i)

    return array