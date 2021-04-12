import numpy as np
import math

__all__ = ['calculate_distance_from_solids2D',
           'calculate_voronois_from_solids2D']

def calculate_distance_from_solids2D(values):
    # grid_cells
    # for all void cells
    # distance to all solidcells for each void cell (0)
    solid_cells=np.where(values>=1)
    void_cells=np.where(values==0)
    result_distances=np.zeros(values.shape)
    for i in range(len(void_cells[0])):
        x=void_cells[0][i]
        y=void_cells[1][i]
        delta_x=x-solid_cells[0]
        delta_y=y-solid_cells[1]
        sum=delta_x*delta_x+delta_y*delta_y
        min_d=np.amin(sum)
        result_distances[x][y]=math.sqrt(min_d)
    return result_distances

def calculate_voronois_from_solids2D(values):
    # grid_cells
    # for all void cells
    # distance to all solidcells
    # asssign solid value of cell with smallest distance. example: if void-cell (0) is closest to cell with value 1 it gets value 1
    solid_cells=np.where(values>=1)
    void_cells=np.where(values==0)
    result_voronoi=np.zeros(values.shape)
    for i in range(len(void_cells[0])):
        x=void_cells[0][i]
        y=void_cells[1][i]
        delta_x=x-solid_cells[0]
        delta_y=y-solid_cells[1]
        sum=delta_x*delta_x+delta_y*delta_y
        min_index=np.argmin(sum)
        result_voronoi[x][y]=values[solid_cells[0][min_index]][solid_cells[1][min_index]]
    return result_voronoi