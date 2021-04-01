
import numpy as np
from .tools import Grid
from .tools import Isovist
from .tools import Shortest_path


__all__ = ['Grid_analytics']

class Grid_analytics(Grid):
    """
    
    Examples
    --------
    >>> from grid_analytics import Grid_analytics

    >>> voxel_space = np.random.randint(2, size=(3,5))
    >>> my_grid = Grid_analytics(voxel_space)
    >>> visbility_map = my_grid.analyse_visibility()
    >>> neighbours_map = my_grid.analyse_neighbours()
    """

    def __init__(self, voxel_map):
        super(Grid, self).__init__()
    
    def analyse_isovist(self, pt):
        pass

    def analyse_visibility(self):
        values = np.full(self.obstacle_map.shape,0)
        for z in range(values.shape[2]):
            values[:, :, z] = self.analyse_visibility_xy(z)
        
        return values

    def analyse_visibility_xy(self, z=0):
        if self.obstacle_map.ndim == 2:
            isovist = Isovist(self.obstacle_map * -1)
        
        else:
            isovist = Isovist(self.obstacle_map[:,:,z] * -1)

        return isovist.isovist_map()

    
    def analyse_shortestpath_xy(self, sp, ep):
        shortestpath = Shortest_path(self.obstacle_map)
        return shortestpath.get_shortest_path(sp, ep)


if __name__ == '__main__':
    pass