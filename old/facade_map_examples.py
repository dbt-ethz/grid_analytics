import numpy as np
import matplotlib.pyplot as plt

from isovist import *
from shortest_path import *

def displayArray(data, height, col='binary', edgecol='w'):

    """
    Display a 2D numpy array using matplotlib
    -
    / Input
    data = 2D numpy array
    height = Height of the plot - Proportional length 
    col = Matplotlib color map for voxels - https://matplotlib.org/stable/gallery/color/colormap_reference.html
    edgecol = Matplotlib color palette for edges - https://matplotlib.org/stable/gallery/color/named_colors.html
    -
    / Output
    Plot a 2D numpy array using matplotlib
    """
    plt.figure(figsize=(height * (data.shape[1] / data.shape[0]), height))
    plt.pcolor(data,cmap=col,edgecolors=edgecol, linewidths=height * 0.06)
    plt.tight_layout()
    plt.show()


height = 20
width = 20

matrix = np.zeros((4),dtype=np.int)
matrix[0] = -1
map1 = np.random.choice(matrix, size=(height, width))
# displayArray(map1, 8, col='binary')

IsoMap1 = Isovist(map1)
startPt = (59,89)
# print(IsoMap1.cell_neighbors(startPt))
# IsoPt = IsoMap1.isovist_from_point(startPt, youAreHere=True, format=1)
# displayArray(IsoPt, 8, col='hot', edgecol='gold')

VisibilityMap1 = IsoMap1.isovist_map_collision(format=1)
# print(IsoMap1.visible_cells)
# print(IsoMap1.invisible_cells)
# VisibilityMap1 = IsoMap1.isovist_map(format=1)
# print(VisibilityMap1)
# print(VisibilityMap1)
displayArray(VisibilityMap1, 8, col='hot', edgecol='gold')
# neighbors = IsoMap1.neighbors_map()
# facade_map = IsoMap1.facade_map()
# print(facade_map)
# displayArray(facade_map, 8, col='hot', edgecol='gold')
# print(neighbors)
# displayArray(tmap1, 8, col='hot', edgecol='gold')

# voxel_space = np.full((nX,nY,nZ),0) # we initialise a 3D Array

# for z in range(nZ):
#     matrix = np.zeros((3),dtype=np.int)
#     matrix[0] = -1
#     map = np.random.choice(matrix, size=(height, width))
#     voxel_space[:,:,z] = map