from __future__ import absolute_import
# 
#  Author: Rongyang Sun <sun-rongyang@outlook.com>
#  Creation Date: 2018-07-11 08:40
#  
#  Description: Extension for alpskit. Utilities for square lattice.
# 
import numpy as np


def get_idx_coor_map(L, W):
  """Get sites index to coordinates mapping.

  :L: int
      Length of the lattice.
  :W: int
      width of the lattice.
  :returns: numpy.ndarray
      coor_at_i_site = returns[idx_at_i_site]

  """
  idx_coor_map = []
  for m in range(L):
    for n in range(W):
      idx_coor_map.append([m, 0])
  return np.array(idx_coor_map)


def get_idx_coor_map_only_len_direction(L, W):
  """Get sites index to coordinates mapping. Only for length direction,
     with width direction is set to 0.

  :L: int
      Length of the lattice.
  :W: int
      width of the lattice.
  :returns: numpy.ndarray
      coor_at_i_site = returns[idx_at_i_site]

  """
  idx_coor_map = []
  for m in range(L):
    for n in range(W):
      idx_coor_map.append([m, 0])
  return np.array(idx_coor_map)
