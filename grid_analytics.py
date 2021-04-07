
import numpy as np
# from .tools import Grid
from .tools import Isovist
from .tools import Shortest_path


# __all__ = ['Grid_analytics']


def analyse_isovist2D(array):
    """
    Analyses 2D visibility for any numpy array >= 2 Dimensions.
    If 3D, XY layers will be analysed

    """
    if array.ndim == 2:
        return _analyse_isovist_xy(array)
    
    elif array.ndim == 3:
        values = np.full(array.shape, 0)
        for z in range(values.shape[2]):
            values[:, :, z] = _analyse_isovist_xy(array[:, :, z])    
        return values

    else:
        raise Exception('array has to be 2D or 3D!!')


def _analyse_isovist_xy(array):
    if array.ndim != 2:
        raise Exception('array has to be 2D!!')
    else:
        isovist = Isovist(array * -1)
    
    return isovist.isovist_map()


def analyse_visibility(array, view_pts=[]):
    if array.ndim == 2:
        return _analyse_visibility_xy(array, view_pts)
    
    elif array.ndim == 3:
        values = np.full(array.shape, 0)
        # view_pts_array = np.full(array.shape, 0)
        # for pt in view_pts:
        #     view_pts_array[pt] = 1
        # for index in np.ndindex(view_pts_array.shape):

        for z in range(values.shape[2]):
            values[:, :, z] = _analyse_visibility_xy(array[:, :, z], view_pts[;, ;, z])    
        return values

    else:
        raise Exception('array has to be 2D or 3D!!')


def _analyse_visibility_xy(array, view_pts=[]):
    if array.ndim != 2:
        raise Exception('array has to be 2D!!')
    else:
        isovist = Isovist(array * -1)
        visibility = np.full(array.shape, 0)
        for pt in view_pts:
            visibility_pt = isovist.isovist_from_point(pt, format=1)
            visibility += visibility_pt
    
    return visibility


def _analyse_shortestpath_xy(array, sp, ep):
    if array.ndim != 2:
        raise Exception('array has to be 2D!!')
    else:
        shortest_path = Shortest_path(array)




# class Grid_analytics(Grid):
#     """
    
#     Examples
#     --------
#     >>> from grid_analytics import Grid_analytics

#     >>> voxel_space = np.random.randint(2, size=(3,5))
#     >>> my_grid = Grid_analytics(voxel_space)
#     >>> visbility_map = my_grid.analyse_visibility()
#     >>> neighbours_map = my_grid.analyse_neighbours()
#     """

#     def __init__(self, voxel_map):
#         super(Grid, self).__init__()
    
#     def analyse_isovist(self, pt):
#         pass

#     def analyse_visibility(self):
#         if self.obstacle_map.ndim == 2:
#             raise Exception('array is not 3D!!!')

#         else:
#             values = np.full(self.obstacle_map.shape,0)
#             for z in range(values.shape[2]):
#                 values[:, :, z] = self.analyse_visibility_xy(z)
            
#             return values

#     def analyse_visibility_xy(self, z=0):
#         if self.obstacle_map.ndim == 2:
#             isovist = Isovist(self.obstacle_map * -1)
        
#         else:
#             isovist = Isovist(self.obstacle_map[:,:,z] * -1)

#         return isovist.isovist_map()

#     def analyse_shortestpath_xy(self, sp, ep):
#         shortestpath = Shortest_path(self.obstacle_map)
#         return shortestpath.get_shortest_path(sp, ep)


if __name__ == '__main__':
    pass