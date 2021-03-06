import numpy as np
# from grid_analytics.isovist import Isovist
from .isovist import Isovist

def distanceSqr(x1, y1, z1, x2, y2, z2):
    dX = x2 - x1
    dY = y2 - y1
    dZ = z2 - z1
    return dX * dX + dY * dY + dZ * dZ


def dot(x1, y1, z1, x2, y2, z2):
    return x1 * x2 + y1 * y2 + z1 * z2

# all vector calculations could be switched to numpy?


def dist_to_ray_sq(px, py, pz, x, y, z, vx, vy, vz):
    c2 = dot(vx, vy, vz, vx, vy, vz)  # can be precalculated
    dx = px - x
    dy = py - y
    dz = pz - z
    c1 = dot(dx, dy, dz, vx, vy, vz)
    if (c1 <= 0):
        return -distanceSqr(px, py, pz, x, y, z)
    b = c1 / c2
    cx = x + b * vx
    cy = y + b * vy
    cz = z + b * vz
    return distanceSqr(px, py, pz, cx, cy, cz)


def shadow_from_sun_ray(voxel_space, sun_vec_x, sun_vec_y, sun_vec_z):
    shadow_space = np.zeros(voxel_space.shape)
    #diag= 0.5**(1.0/3)
    diag = 0.25
    it = np.nditer(voxel_space, flags=['multi_index'])
    for x in it:
        if x == 1:  # solid
            x1, y1, z1 = it.multi_index[0], it.multi_index[1], it.multi_index[2]
            if shadow_space[it.multi_index] == 0:  # not yet shadow
                it2 = np.nditer(voxel_space, flags=['multi_index'])
                for t in it2:
                    if t == 1:  # another solid
                        if shadow_space[it2.multi_index] == 0:  # not yet shadow
                            x, y, z = it2.multi_index[0], it2.multi_index[1], it2.multi_index[2]
                            if (x != x1 or y != y1 or z != z1):  # don't check yourself
                                dist = dist_to_ray_sq(
                                    x, y, z, x1, y1, z1, sun_vec_x, sun_vec_y, sun_vec_z)
                                if (dist >= 0 and dist < diag):  # does the shadow ray hit this cell?
                                    shadow_space[it2.multi_index] = 1
    return shadow_space


def analyze_3d_grid(model3d, analysis_type="facade", ray1 = (1,1,0) ):

    if analysis_type == "facade":
        facade_map = facade_voxel(model3d)

        array3d = facade_map


    elif analysis_type == "shadow":

        shadow_map=shadow_from_sun_ray(model3d,ray1[0],ray1[1],ray1[2])

        array3d = shadow_map

    elif analysis_type == "visibility":
        array3d = visibility_voxel(model3d)

    return array3d


def visibility_voxel(voxel_space):
    
    voxel_space = voxel_space * -1
    
    color = np.full((*voxel_space.shape,3),1)

    visibility_voxel = np.full(voxel_space.shape,0)
    for z in range(voxel_space.shape[2]):
        map = voxel_space[:,:,z]
        iso_map = Isovist(map)
        visibility_map = iso_map.isovist_map_collision(format=1)
        visibility_voxel[:, :, z] = visibility_map

    return visibility_voxel

def facade_voxel(voxel_space):
    voxel_space = voxel_space * -1
    
    color = np.full((*voxel_space.shape,3),1)

    facade_analyse_voxel = np.full(voxel_space.shape,0)
    for z in range(voxel_space.shape[2]):
        map = voxel_space[:,:,z]
        iso_map = Isovist(map)
        facade_map = iso_map.facade_map()
        facade_analyse_voxel[:, :, z] = facade_map

    return facade_analyse_voxel

