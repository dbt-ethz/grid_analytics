import grid_analytics as ga
import numpy as np

nX, nY, nZ = 5, 5, 5

voxel_space1 = np.full((nX, nY, nZ), 0)
voxel_space1[0:1,0:2,:] = 1

vec = [1, 2, 0]
voxel_space2 = ga.array_move(voxel_space1, vec)
voxle_union = ga.array_union(voxel_space1, voxel_space2)

ga.display_array3D(voxle_union, width=8, height=8)