import numpy as np


__all__ = ['union', 'intersection', 'difference']


def union(array1, array2):
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


def intersection(array1, array2):
    return np.logical_and(array1, array2)


def difference(array1, array2):
    return np.logical_and(array1, np.logical_not(array2))