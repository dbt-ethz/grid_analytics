
import numpy as np
from .tools import Isovist
from .tools import Shortestpath
from .tools import get_neighbors2D
from .tools import get_neighbors3D
from .tools import calculate_distance_from_solids2D
from .tools import calculate_voronois_from_solids2D
from .tools import analyse_shadow_Bresenham_sorted


__all__ = [
    'analyse_neighbours2D',
    'analyse_neighbours3D',
    'analyse_isovist_map2D',
    'analyse_isovist2D',
    'analyse_shortestpath2D',
    'analyse_centrality2D',
    'analyse_shadow',
    'analyse_distances2D',
    'analyse_voronoi2D'
]


def analyse_neighbours2D(array):

    """
    Returns the amount of 2d neighbours per cell for any 2D or 3D array
    
    Parameters
    ----------
    array: numpy ndarray
        2D or 3D numpy array with 0 for void cells, 1 for solid cells

    Returns
    -------
    numpy array
        2D or 3D numpy array of values representing how many solid  are seen per cell.

    Examples
    --------
    >>>
    >>>
    >>>
    """

    if array.ndim == 2:
        values = np.full(array.shape, 0)
        for x, y in np.ndindex(array.shape):
            # only evaluate solid voxels
            if array[x, y] > 0:
                values[x][y] = get_neighbors2D(array, x, y)

        return values
    
    elif array.ndim == 3:
        values = np.full(array.shape, 0)
        for x, y, z in np.ndindex(array.shape):
            # only evaluate solid voxels
            if array[x, y, z] > 0:
                array_slice = array[:, :, z].reshape(array.shape[:2])
                values[x][y][z] = get_neighbors2D(array_slice, x, y)

        return values
    else:
        raise Exception('array has to be 2D or 3D!!')


def analyse_neighbours3D(array):

    if array.ndim == 2:
        values = np.full(array.shape, 0)
        for x, y in np.ndindex(array.shape):
            # only evaluate solid voxels
            if array[x, y] > 0:
                values[x][y] = get_neighbors2D(array, x, y)

        return values
    
    elif array.ndim == 3:
        values = np.full(array.shape, 0)
        for x, y, z in np.ndindex(array.shape):
            # only evaluate solid voxels
            if array[x, y, z] > 0:
                values[x][y][z] = get_neighbors3D(array, x, y, z)

        return values
        
    else:
        raise Exception('array has to be 2D or 3D!!')


def analyse_isovist_map2D(array, radius=None, mode='void'):
    """
    Analyses 2D visibility for any numpy array >= 2 Dimensions.
    If 3D, XY layers will be analysed
    
    Parameters
    ----------
    array: numpy ndarray
        2D or 3D numpy array with 0 for void cells, 1 for solid cells
    mode: string
        string 'void' or 'solid'. 'void' returns isovist map of all void cells.
        'solid' returns isovist map of all solid cells


    Returns
    -------
    numpy array
        2D or 3D numpy array of values representing how many cells are seen per cell.

    Examples
    --------
    >>> import numpy as np
    >>> array = np.random.randint(2, size=(2, 4))
    >>> isovist_map = analyse_isovist_map2D(array, mode='solid')
    """
    if array.ndim == 2:
        return _analyse_isovist_map_xy(array, radius, mode)
    
    elif array.ndim == 3:
        values = np.full(array.shape, 0)
        for z in range(values.shape[2]):
            values[:, :, z] = _analyse_isovist_map_xy(array[:, :, z], radius, mode)    
        return values

    else:
        raise Exception('array has to be 2D or 3D!!')


def _analyse_isovist_map_xy(array, radius=None, mode='void'):
    isovist = Isovist(array * -1, radius)

    if mode == 'void':
        return isovist.isovist_map(format=1)
    elif mode == 'solid':
        return isovist.isovist_map_collision(format=1)
    else:
        return


def analyse_isovist2D(array, radius=None, view_point=[0,0]):
    """ Analyses 2D visibility for any numpy array >= 2 Dimensions.
    Based on a given viewpoint.

    Parameters
    ----------
    array: numpy ndarray
        2D or 3D numpy array with 0 for void cells, 1 for solid cells
    view_point: list or tuple
        the index of the viewpoint in the array.
        It needs to be inside of the array and have same dimension with the array

    Returns
    -------
    numpy ndarray
        2D or 3D numpy array with 1 for visible cells, 0 for invisible cells, -1 for solid cells.
    """
    if array.ndim == 2:
        return _analyse_isovist_map_xy(array, radius, view_point)
    
    elif array.ndim == 3:
        raise NotImplementedError

    else:
        raise Exception('array has to be 2D or 3D!!')


def _analyse_isovist_xy(array, radius, view_point):
    isovist = Isovist(array * -1, radius)
    return isovist.isovist_from_point(view_point, format=1)


def analyse_shortestpath2D(array, sp, ep):
    """ Analyses the shortest path in a 2D numpy array.
    
    Parameters
    ----------
    array: numpy ndarray
        2D or 3D numpy array with values of 0 and 1
    sp: list or tuple
        the index of the starting point in the array.
        It needs to be inside of the array and have same dimension with the array
    ep: list or tuple
        the index of the ending point in the array.
        It needs to be inside of the array and have same dimension with the array  
    
    Returns
    -------
    numpy ndarray
        2D or 3D numpy array with 1 for path cells, 0 for the rest of void cells, -1 for solid cells.
    """
    if array.ndim == 2:
        return _analyse_shortestpath_xy(array, sp, ep)
    
    elif array.ndim == 3:
        raise NotImplementedError

    else:
        raise Exception('array has to be 2D or 3D!!')


def _analyse_shortestpath_xy(array, sp, ep):
    shortest_path = Shortestpath(array * -1)
    return shortest_path.get_shortest_path(sp, ep, format=1)


def analyse_centrality2D(array):
    """
    Returns centrality map
    
    Parameters
    ----------
    array: numpy ndarray
        2D or 3D numpy array with values of 0 and 1
    
    Returns
    -------
    numpy ndarray:
        numpy array with centrality percentage for each cell
    """
    if array.ndim == 2:
        return _analyse_centrality_xy(array)
    
    elif array.ndim == 3:
        raise NotImplementedError

    else:
        raise Exception('array has to be 2D or 3D!!')


def _analyse_centrality_xy(array):
    shortest_path = Shortestpath(array * -1)
    return shortest_path.get_centrality(format=1)


def analyse_shadow(array, light_vectors):
    """Analyses shadow for any 3D array

    Parameters
    ----------
    array: numpy ndarray
        2D or 3D numpy array with values of 0 and 1
    light_vectors: list of vectors(tuple of 3 float)
        vectors represent light direction
    
    Returns
    -------
    numpy ndarray:
        numpy array with 1 as shadow, 0 as not in shadow
    """
    shadow_map = np.zeros(array.shape, dtype=int)
    for vec in light_vectors:
        light = np.array(vec, dtype=np.float)
        shadow_map += analyse_shadow_Bresenham_sorted(array, light)
    
    return shadow_map


def analyse_distances2D(array):
    """
    Returns the distances of void cells to their closest solid cells 
    
    Parameters
    ----------
    array: numpy ndarray
        2D or 3d numpy array with 0 for void cells, and >1 for solid cells

    Returns
    -------
    numpy array
        2D or 3d numpy array of values representing the index of a solid cell which is closest to a void

    """

    if array.ndim == 2:
        values = calculate_distance_from_solids2D(array)

        return values
    
    elif array.ndim == 3:

        values = np.full(array.shape, 0)
        for z in range(values.shape[2]):
            array_slice = array[:, :, z].reshape(array.shape[:2])
            values[:, :, z] = calculate_distance_from_solids2D(array_slice)   

        return values
    
    else:
        raise Exception('array has to be 2D or 3D!!')


def analyse_voronoi2D(array):
    """
    Returns the indices of the solid cell which is closer to every void cell 
    
    Parameters
    ----------
    array: numpy ndarray
        2D or 3d numpy array with 0 for void cells, and >1 for solid cells

    Returns
    -------
    numpy array
        2D or 3d numpy array of values representing the index of a solid cell which is closer every void cell

    """

    if array.ndim == 2:
        values = calculate_voronois_from_solids2D(array)

        return values
    
    elif array.ndim == 3:

        values = np.full(array.shape, 0)
        for z in range(values.shape[2]):
            array_slice = array[:, :, z].reshape(array.shape[:2])
            values[:, :, z] = calculate_voronois_from_solids2D(array_slice)   

        return values
    
    else:
        raise Exception('array has to be 2D or 3D!!')


if __name__ == '__main__':
    pass