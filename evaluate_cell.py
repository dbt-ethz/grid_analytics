import numpy as np


def _find_2d_neighbors(matrix, rowNumber, colNumber):
    """
    Returns the 4 neighbors of a cell in a 2d numpy array if they exist.

    Arguments
    ----------
    cells : numpy.ndarray
        Numpy Array of shape (nX,nY)
    rowNumber: integer
        row the cell belongs to
    colNumber: integer
        column the cell belongs to
    """

    result = []
    # top
    if rowNumber > 0:
        result.append(matrix[rowNumber-1][colNumber])
    # bottom
    if rowNumber < matrix.shape[0]-1:
        result.append(matrix[rowNumber+1][colNumber])
    # left
    if colNumber > 0:
        result.append(matrix[rowNumber][colNumber-1])
    # right
    if colNumber < matrix.shape[1]-1:
        result.append(matrix[rowNumber][colNumber+1])

    return result


def calculate_number_of_facades(cells):
    """
    Returns the amount of free facades of a floorplan.

    Arguments
    ----------
    cells : numpy.ndarray
        Numpy Array of shape (nX,nY,nZ) and dtype=int where positive value corresponds to a Solid voxel
    """

    total = 0

    for row, col, lev in np.ndindex(cells.shape):

        # only evaluate solid voxels
        if cells[row, col, lev] > 0:
            in_2d = cells[:, :, lev].reshape(
                (cells.shape[0], cells.shape[1]))
            neighbors = _find_2d_neighbors(in_2d, row, col)
            total += (4-len(neighbors))
            for n in neighbors:
                if n == 0:
                    total += 1
    return total


def calculate_compactness(cells):
    """
    Returns the compactness of a floorplan as the ratio between area and perimeter.
    """
    perimeter = calculate_number_of_facades(cells) * 1
    area = 1 * 1 * np.count_nonzero(cells)

    if perimeter > 0:
        compactness = area/perimeter
    else:
        compactness = 0

    return compactness


def calculate_room_adjacencies(cells, n):
    """
    Returns the amount of cells that have n neighbors
    """
    pass


def calculate_patios(cells):

    pass


def calculate_stability(cells):
    pass


def calculate_daylight(cells):
    pass
