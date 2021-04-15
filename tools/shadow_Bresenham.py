import numpy as np
from numba import jit


__all__ = ['analyse_shadow_Bresenham_sorted']


@jit
def _Bresenham_line_3D(array, vec, start_pt):
    ''' creata a Bresenham line in 3D numpy array
    '''
    dx, dy, dz = vec
    deltaerr_y = abs(dy / dx)
    deltaerr_z = abs(dz / dx)
    x, y , z = start_pt
    if dy > 0:
      y_sign = +1
    else:
      y_sign = -1
    if dz > 0:
      z_sign = +1
    else:
      z_sign = -1
    error_y = 0
    error_z = 0
    first_point = True

    while True:
        # Exit condition when drawing out of boundary
        if x < 0:
          return array
        if y < 0:
          return array
        if z < 0:
          return array
        if x >= array.shape[0]:
          return array
        if y >= array.shape[1]:
          return array
        if z >= array.shape[2]:
          return array
          
        # Mark line voxel except first point
        if first_point:
          first_point = False
        else:
          # array[x, y, z] = True
          array[int(x), int(y), int(z)] = True
        # Increment line
        error_y += deltaerr_y
        if error_y >= 0.5:
            y += y_sign
            error_y -= 1

        error_z += deltaerr_z
        if error_z >= 0.5:
            z += z_sign
            error_z -= 1

        x += dx//abs(dx)

    return array


@jit
def Bresenham_line_3D(array, vec, start_pt):
    # swtiching order
    vec_abs = np.absolute(vec)
    sign = np.sign(vec)

    # switch_order = np.argsort(vec_abs)[::-1]
    # switch_back_order = np.argsort(switch_order)

    if vec_abs[0] > vec_abs[1]:
      if vec_abs[0] > vec_abs[2]:
        # 0 is largest
        switch_order, switch_back_order = (0,1,2), (0,1,2)
      else:
        # 2 is largest
        switch_order, switch_back_order = (2,1,0), (2,1,0)
    else:
      if vec_abs[1] > vec_abs[2]:
        # 1 is largest
        switch_order, switch_back_order = (1,0,2), (1,0,2)
      else:
        # 2 is largest
        switch_order, switch_back_order = (2,1,0), (2,1,0)


    # swtich vec
    vec_switched_xyz = np.sort(vec_abs)[::-1]
    switch_sign = np.array([sign[switch_order[0]], sign[switch_order[1]], sign[switch_order[2]]])
    vec_switched_xyz = vec_switched_xyz * switch_sign

    #switch start pt
    pt_switched = np.array([start_pt[switch_order[0]], start_pt[switch_order[1]], start_pt[switch_order[2]]])

    #swtich result array
    array = np.transpose(array, switch_order)

    # make line
    array = _Bresenham_line_3D(array, vec_switched_xyz, pt_switched)

    # switch returned array
    array= np.transpose(array, switch_back_order)

    return array


def analyse_shadow_Bresenham(voxel_space, light):
    shadows = np.zeros(shape=voxel_space.shape, dtype=bool)
    for index in np.ndindex(voxel_space.shape):
        if voxel_space[index] and not shadows[index]:
            ray = Bresenham_line_3D(shadows, light, index)

    return np.logical_and(voxel_space, shadows)


def analyse_shadow_Bresenham_sorted(voxel_space, light):
    # Initialize empty canvas to keep shadows
    shadows = np.zeros(shape=voxel_space.shape, dtype=np.bool_)
    indices = np.transpose(np.nonzero(voxel_space))
    sort = np.argsort(np.dot(indices, light))

    sort = np.argsort(np.dot(indices, light))
    for index in indices[sort]:
        if not shadows[index[0], index[1], index[2]]:
            ray = Bresenham_line_3D(shadows, light, index)

    return np.logical_and(voxel_space, shadows)