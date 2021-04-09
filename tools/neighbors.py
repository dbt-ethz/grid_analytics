import numpy as np

__all__ = ['get_neighbors2D',
           'get_neighbors3D']

def get_neighbors2D(model_2d, row, col):
    """
    returns the ammount of solid cells around a cell in 2d
    """

    #add a border of 0 around the 2d array
    model_2d = np.pad(model_2d, pad_width =1, mode ='constant', constant_values=0)
    #shift position to reflect the new index
    row +=1
    col +=1

    neighbors = []
    # edge connected neighbors 
    # north
    neighbors.append(model_2d[row-1][col])
    # south
    neighbors.append(model_2d[row+1][col])
    # west
    neighbors.append(model_2d[row][col-1])
    # east
    neighbors.append(model_2d[row][col+1])

    #corner connected neighbors

    return np.count_nonzero(neighbors)

  def get_neighbors3D(model_3d, row, column, level):
    
    # returns the ammount of solid cells around a cell in a 3d

    #add a border of 0 around the 3d array
    model_3d = np.pad(model_3d, pad_width =1, mode ='constant', constant_values=0)
    #shift position to reflect the new index
    row +=1
    col +=1
    level +=1

    neighbors = []
    # face connected neighbors 
    # north
    neighbors.append(model_2d[row-1][col][level])
    # south
    neighbors.append(model_2d[row+1][col][level])
    # west
    neighbors.append(model_2d[row][col-1][level])
    # east
    neighbors.append(model_2d[row][col+1][level])
    # top
    neighbors.append(model_2d[row][col][level+1])
    # bottom
    neighbors.append(model_2d[row][col][level-1])

    #edge connected neighbors

    #corner connected neighbors

    return np.count_nonzero(neighbors)


# def _get_neighboursND(p, exclude_p=True, shape=None):
#     ndim = len(p)
#     # generate an (m, ndims) array containing all strings over the alphabet {0, 1, 2}:
#     offset_idx = np.indices((3,) * ndim).reshape(ndim, -1).T
#     # use these to index into np.array([-1, 0, 1]) to get offsets
#     offsets = np.r_[-1, 0, 1].take(offset_idx)
#     # optional: exclude offsets of 0, 0, ..., 0 (i.e. p itself)
#     if exclude_p:
#         offsets = offsets[np.any(offsets, 1)]
#     neighbours = p + offsets    # apply offsets to p
#     # optional: exclude out-of-bounds indices
#     if shape is not None:
#         valid = np.all((neighbours < np.array(shape)) & (neighbours >= 0), axis=1)
#         neighbours = neighbours[valid]
#     return neighbours