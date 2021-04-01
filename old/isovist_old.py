# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Remy Clemente']
__copyright__  = 'Copyright 2021 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import numpy as np


class Isovist:
    """A class to compute isovist using numpy
    (https://en.wikipedia.org/wiki/Isovist)
    (https://numpy.org/)

    Attributes 
    ----------
    obstacle_map : 2D numpy array 
            -1 for collision and 0 for ground
    
    Methods
    -------
    isovist_from_point(startIndex, youAreHere=False, format=0)
            Create a 1D or 2D isovist numpy array from a starting point
    -
    isovist_map(format=0)
            Create a 1D or 2D isovist numpy array with visibility percentage of each cell
    """

    def __init__(self, obstacle_map):
        self.obstacle_map = obstacle_map
    
    @property
    def visible_cells(self):
        return np.argwhere(self.obstacle_map==0)

    @property
    def invisible_cells(self):
        return np.argwhere(self.obstacle_map==-1)
    
    @property
    def edges(self):
        coords_arrs = np.mgrid[0:self.obstacle_map.shape[0], 0:self.obstacle_map.shape[1]]
        edges = [np.concatenate([
            arr[0,:-1],
            arr[:-1,-1],
            arr[-1,::-1],
            arr[-2:0:-1,0]]) for arr in coords_arrs]
        return edges

    def cell_neighbors(self, cell_index):
        x, y = cell_index
        neighbors = [
            (x-1, y),
            (x, y-1),
            (x+1, y),
            (x, y+1)
        ]

        def out_of_boundary(index):
            if index[0] < 0 or index[0] > self.obstacle_map.shape[0]-1 or index[1] < 0 or index[1] > self.obstacle_map.shape[1]-1:
                return True
            else:
                return False
        
        neighbors = [nbr for nbr in neighbors if not out_of_boundary(nbr)]

        return neighbors

    def neighbors_map(self):
        neighbors_map = np.ones(self.obstacle_map.shape, dtype=np.int) * -1

        for cell in self.invisible_cells:
            facade_count = 0
            neighbors = self.cell_neighbors(cell)
            for nbr in neighbors:
                if self.obstacle_map[nbr[0], nbr[1]] == -1:
                    facade_count += 1
            neighbors_map[cell[0], cell[1]] = facade_count
        
        return neighbors_map

    def facade_map(self):
        return 4 - self.neighbors_map()

    def isovist_from_point(self, startIndex, youAreHere=False, format=0):
        """
        Create a 2D or 1D isovist numpy array from a starting point
        
        Parameters
        ----------
        startIndex : pov point (x,y)
        youAreHere : Boolean to highlight pov with value -2
        format : 0 for 1D numpy array ouput /    1 for 2D numpy array output
        
        Returns
        -------
        isovist_area : Isovist Map with -1 collision, 0 non-visible ground, 1 visible ground
        """
        isovist_area = np.copy(self.obstacle_map)
        
        # Shoot rays
        for xEdg, yEdg in zip(self.edges[0], self.edges[1]):
            self.visibility_ray(startIndex, (yEdg, xEdg), isovist_area)
        
        # Highlight pov
        if youAreHere:
                isovist_area[startIndex[1], startIndex[0]] = -2

        # Export options
        if format == 0:
                return isovist_area.flatten()
        elif format == 1:
                return isovist_area
    
    def isovist_map(self, format=0):
        """
        Create a 1D or 2D isovist numpy array with visibility percentage for each cell
        
        Parameters
        ----------
        format : 0 for 1D numpy array ouput / = 1 for 2D numpy array output
        

        Returns
        -------
        isovist_map : Isovist for each cell in a 1D or 2D numpy array 
        """
        
        isovist_map = np.copy(self.obstacle_map)

        # Shoot rays and count enlightened cells
        povMap = np.zeros(self.obstacle_map.shape, dtype=np.int)
        for [startX, startY] in self.visible_cells:
                for xEdg, yEdg in zip(self.edges[0], self.edges[1]):
                        self.visibility_ray((startY, startX), (yEdg, xEdg), povMap)    

                # Percentage of visibility per cell
                isovist_map[startX, startY] = (np.count_nonzero(povMap) / self.visible_cells.size) * 100
                povMap = np.zeros(self.obstacle_map.shape, dtype=np.int)

        # Export options
        if format == 0:
                return isovist_map.flatten()
        elif format == 1:
                return isovist_map
    
    
    def visibility_ray(self, startIndex, endIndex, visibility_map):
        """
        Bresenham's Line Algorithm using np array to detect collision
        
        Parameters
        ----------
        startIndex : (x,y) corrdinates of ray's starting point
        endIndex : (x,y) coordinates of ray's ending point
        visibility_map : 2D numpy array to be updated

        Returns
        -------
        visibility_map updated with the shooted ray
        """
        
        # Setup initial conditions
        x1, y1 = startIndex
        x2, y2 = endIndex
        dx = x2 - x1
        dy = y2 - y1
        
        # Determine how steep the line is
        is_steep = abs(dy) > abs(dx)
        
        # Rotate line
        if is_steep:
                x1, y1 = y1, x1
                x2, y2 = y2, x2
        
                # Recalculate differentials
                dx = abs(x2 - x1)
                dy = abs(y2 - y1)
                
                # Calculate error
                error = int(dx / 2.0)
                ystep = 1 if y1 < y2 else -1
                
                # Inverse orientation
                incr = 1 if x1 < x2 else -1
                
                # Iterate over bounding box generating points between start and end
                y = y1
                for x in range(x1, x2 + incr, incr):
                        if not self.obstacle_map[x,y] < 0:
                            visibility_map[x,y] = 1
                            error -= abs(dy) 
                            if error < 0:
                                    y += ystep
                                    error += dx
                        else:
                                break
        else:
                # Recalculate differentials
                dx = abs(x2 - x1)
                dy = abs(y2 - y1)
                
                # Calculate error
                error = int(dx / 2.0)
                ystep = 1 if y1 < y2 else -1
                
                # Inverse orientation
                incr = 1 if x1 < x2 else -1
                
                # Iterate over bounding box generating points between start and end
                y = y1
                for x in range(x1, x2 + incr, incr):
                        if not self.obstacle_map[y,x] < 0:
                            visibility_map[y,x] = 1
                            error -= abs(dy) 
                            if error < 0:
                                    y += ystep
                                    error += dx
                        else:
                                break