import numpy as np


__all__ = ['Grid']


class Grid:
    """ 2D or 3D voxel space """

    def __init__(self, voxel_map):
        self._obstacle_map = None
        self.obstacle_map = voxel_map
        
    @property
    def obstacle_map(self):
        return self._obstacle_map
    
    @obstacle_map.setter
    def obstacle_map(self, voxel_map):
        if voxel_map.ndim > 3 or voxel_map.ndim < 2:
            raise Exception('array has to be 2D or 3D!!')
        else:
            # convert any input into array of 0 and 1
            voxel_map = voxel_map > 0
            voxel_map = voxel_map * 1
            self._obstacle_map = voxel_map
    
    @property
    def visible_cells(self):
        pass

    @property
    def invisible_cells(self):
        pass


if __name__ == '__main__':
    pass
