from __future__ import absolute_import
# 
#  Author: Rongyang Sun <sun-rongyang@outlook.com>
#  Creation Date: 2018-07-31 23:11
#  
#  Description: Extension for alpskit. Utilities for chain lattice.
# 
import numpy as np


def get_idx_coor_map(L):
  """Get sites index to coordinates(2 dimensions) mapping.

  :L: int
      Length of the lattice.
  :returns: numpy.ndarray
      coor_at_i_site = returns[idx_at_i_site]

  """
  idx_coor_map = []
  for m in range(L):
    idx_coor_map.append([m, 0])
  return np.array(idx_coor_map)
