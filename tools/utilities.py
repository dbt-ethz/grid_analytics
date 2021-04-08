import numpy as np


__all__ = ['array_union', 'array_intersection', 'array_difference','array_move']


def array_union(array1, array2):
    """ boolean union 2 voxel spaces.

    Parameters
    ----------
    array1: numpy ndarray
        numpy array with values of 0 and 1. 0 represents void cell and 1 represents solid.
    array2: numpy ndarray
        numpy array with values of 0 and 1. 0 represents void cell and 1 represents solid.
    
    Returns
    -------
    numpy ndarray
    """
    return np.logical_or(array1, array2)


def array_intersection(array1, array2):
    return np.logical_and(array1, array2)


def array_difference(array1, array2):
    return np.logical_and(array1, np.logical_not(array2))


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