#!/usr/bin/env python`
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Remy Clemente']
__copyright__  = 'Copyright 2021 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import numpy as np

class Shortestpath:
  """Graph analytic's class to compute betweenness centrality using numpy
  (https://en.wikipedia.org/wiki/Betweenness_centrality)
  (https://numpy.org/)
  

  Attributes 
  ----------
  obstacle_map : 2D numpy array 
      -1 for collision and 0 for ground
  
  Methods
  ----------
  get_minimal_spanningtree(startIndex, youAreHere=False, format=0)
      Dijkstra's algorithm to compute distances from one cell and minimal spanning tree
  -
  get_shortest_path(startIndex, endIndex, youAreHere=False, format=0)
      Shortest path between two cells
  -
  get_centrality(format=0)
      Centrality map
  -
  get_traffic(format=0)
      Traffic map
  """
  

  def __init__(self, obstacle_map):
    self.obstacle_map = obstacle_map
    self.visible_cells = np.argwhere(obstacle_map==0)
    self.nbarr = self.get_1D_neighbors()
  
  
  def indexFromXY(self, x, y, nY):
    """
    1D index from a 2D array
    """
    return x*nY + y
  
  
  def get_1D_neighbors(self):
    """
    Compute 1D np array with 8 neighbor cell's keys from 2D np array
    
    Returns
    -------
    nb : 1D numpy array (with (map.size,8) as shape) with 8 neighbor cell's 1D keys
    """
    adjacents = [(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1)]
    
    nb = np.full((self.obstacle_map.size,8), -1, dtype=np.int)
    
    for [x,y] in self.visible_cells:
        index_1D = self.indexFromXY(x,y,self.obstacle_map.shape[1])
        for i, (xpos,ypos) in enumerate(adjacents):
            if 0 <= x+xpos < self.obstacle_map.shape[0] and 0 <= y+ypos < self.obstacle_map.shape[1]:
                if not self.obstacle_map[x+xpos, y+ypos] < 0:
                    nb[index_1D, i] = self.indexFromXY(xpos+x, ypos+y, self.obstacle_map.shape[1])
    return nb
  
  
  def get_minimal_spanningtree(self, startIndex, youAreHere=False, format=0):
    """
    Dijkstra's algorithm to compute distances from one cell and minimal spanning tree
    
    Parameters
    ----------
    startIndex : 1D key of start cell (x*nY + y)
    youAreHere : Boolean to highlight pov by newMap[start] = -2
    format : 0 for 1D numpy array / 1 for 2D numpy array
    
    Returns
    -------
    distArr : 1D or 2D numpy array with distances from start cell
    predArr : 1D or 2D numpy array with closest coordinates from start cell (minimal spanning tree)
    """
    
    # Vectorized shortest distance
    distArr = np.where(self.obstacle_map.flatten() < 0, -1, np.full(self.obstacle_map.size, np.inf))
    distArr[startIndex] = 0
    indexes = np.full((self.obstacle_map.size), -1, dtype=np.int)
    predArr = np.full((self.obstacle_map.size), -1, dtype=np.int)
    
    check = np.where(distArr==0)[0]
    nNew = check.size
    indexes[0:nNew] = check
    predArr[0:nNew] = check
    endI = nNew
    weights = [1.4, 1, 1.4, 1, 1.4, 1, 1.4, 1]
    
    while nNew > 0:
        nNew = 0
        for i in range(endI):
            cellIndex = indexes[i]
            if not cellIndex < 0: 
                nbrs = self.nbarr[cellIndex]
                for j, nbr in enumerate(nbrs):
                    if not nbr < 0:
                        cost = distArr[cellIndex] +  weights[j] 
                        if distArr[nbr] > cost:
                            distArr[nbr] = cost
                            indexes[endI+nNew] = nbr
                            predArr[nbr] = cellIndex
                            nNew += 1
        
        indexes[0 : nNew] = indexes[endI : endI + nNew]
        endI = nNew
    
    distArr = np.where(distArr == np.inf, -1, distArr)
    
    # Highlight pov
    if youAreHere:
        distArr[startIndex] = np.inf
    
    if format == 0:
        return distArr, predArr
    
    elif format == 1:
        # Reshape (1D -> 2D) and Rewrite infinities (inf -> -1)
        distArr = np.reshape(distArr, self.obstacle_map.shape)
        
        # Reshape (1D -> 2D) closest neighbor key from start cell
        p = np.full((self.obstacle_map.size,2), -1, dtype=np.int)
        for i, _ in enumerate(predArr):
            if not _ < 0:
                p[i] = [int(_/self.obstacle_map.shape[1]), int(_%self.obstacle_map.shape[1])]
        p = np.reshape(p,(*self.obstacle_map.shape, 2))
        
        return distArr, p
  
  
  def get_shortest_path(self, startIndex, endIndex, youAreHere=False, format=0):
    """
    Shortest path between two cells
    
    Parameters
    ----------
    startIndex : 1D key of start cell
    endIndex : 1D key of end cell
    youAreHere : Boolean to highlight pov by newMap[start] = -2
    format : 0 for 1D numpy array / 1 for 2D numpy array
    
    Returns
    -------
    visibility_map updated with the shooted ray
    """
    shortestPath_map = np.copy(self.obstacle_map.flatten())
    
    pred = self.get_minimal_spanningtree(startIndex)[1]
    self.get_path(startIndex, endIndex, pred, shortestPath_map)
    
    # Export options
    if format == 0:
        return shortestPath_map
    elif format == 1:
        return np.reshape(shortestPath_map, self.obstacle_map.shape)
  
  
  def get_path(self, startIndex, endIndex, predArr, visible_map):
    """
    Find path between two cells based on minimim spanning tree
    
    Parameters
    ----------
    startIndex : 1D key of start cell
    endIndex : 1D key of end cell
    predArr : 1D numpy array with closest coordinates from startIndexes
    visible_map : 1D numpy array with -1 for collision and 0 for ground
    
    Returns
    -------
    Update visible_map with 1 for path cells, 0 for ground and -1 for collision
    """
    visible_map[endIndex] += 1
    v = predArr[endIndex]
    
    while v != startIndex:
        visible_map[v] += 1
        v = predArr[v]
    visible_map[startIndex] += 1
  
  
  def get_centrality(self, format=0):
    """
    Return centrality map
    
    Parameters
    ----------
    format : 0 for 1D numpy array / 1 for 2D numpy array
    
    Returns
    -------
    centralityMap : 1D or 2D numpy array with centrality percentage for each cell
    """
    centralityMap = np.zeros(self.obstacle_map.size, dtype=np.float32)
    
    # Ground cells
    vCells = np.argwhere(self.obstacle_map.flatten() == 0).flatten()
    
    for k in vCells:
      dist = self.get_minimal_spanningtree(k)[0]
      centralityMap[k] = dist[dist > 0].sum() / np.sum(dist > 0)
    
    if format == 0:
      return centralityMap
    elif format == 1:
      return np.reshape(centralityMap, self.obstacle_map.shape)
  
  
  def get_cell_traffic(self, startIndex, traffic_map):
    """
    Return traffic of a specific cell
    
    Parameters
    ----------
    startIndex : 1D key of start cell
    traffic_map : 1D numpy array
    
    Returns
    -------
    traffic_map updated from startIndex cell traffic
    """    
    pred = self.get_minimal_spanningtree(startIndex)[1]
    pr = np.concatenate(np.argwhere(pred > 0))
    
    for p in pr:
        self.get_path(startIndex, p, pred, traffic_map)
  
  
  def get_traffic(self, format=0):
    """
    Traffic map
    
    Parameters
    ----------
    format : 0 for 1D numpy array / 1 for 2D numpy array
    
    Returns
    -------
    trafficMap : 1D or 2D numpy array with traffic values
    """
    
    trafficMap = np.zeros(self.obstacle_map.size,dtype=np.int)

    # Ground cells
    vCells = np.argwhere(self.obstacle_map.flatten()==0).flatten()
    
    # Update traffic map
    for k in vCells:
        self.get_cell_traffic(k, trafficMap)
    
    if format == 0:
      return trafficMap
    elif format == 1:
      return np.reshape(trafficMap, self.obstacle_map.shape)