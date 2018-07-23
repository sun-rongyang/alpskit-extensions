from __future__ import absolute_import
# 
#  Author: Rongyang Sun <sun-rongyang@outlook.com>
#  Creation Date: 2018-07-10 16:51
#  
#  Description: Extension for alpskit. MPS simulation measurement.
# 
import alpskit.data as akd
from . import squarelattice as sl

from copy import deepcopy

import numpy as np


def measu_hole_msd_vs_time(case_data):
  """Measure hole MSD (<r^2>) vs. time. Just for ONE hole case. 

  :case_data: str
      Data folder to contain the data JSON files for the case.
  :returns: alpskit.data.MeasuData
      MSD vs. time data.

  """
  orig_data_file_name = 'local_n_vs_tau.json'
  local_n_vs_tau = akd.js_to_measu_data(case_data +'/'+ orig_data_file_name)
  L = int(local_n_vs_tau.props['L'])
  W = int(local_n_vs_tau.props['W'])
  local_hole_vs_tau_data = 1 - local_n_vs_tau.y
  idx_coor_map = sl.get_idx_coor_map(L, W)
  msd = _get_msd(local_hole_vs_tau_data, idx_coor_map, L)
  tau = np.array(local_n_vs_tau.x)
  props = dict(local_n_vs_tau.props)
  props['observation'] = 'MSD vs. time'
  props['xlabel'] = r'$\tau$'
  props['ylabel'] = r'$<\hat{r}^2>$'
  return akd.MeasuData(tau, msd, props)


def measu_msd_exponent_vs_ln_tau(hole_msd_vs_time):
  """Measure MSD exponent vs. ln tau from MSD data.

  :hole_msd_vs_time: MeasuData
      Hole MSD vs. time data.
  :returns: MeasuData
      MSD exponent vs. ln tau.

  """
  hole_msd_vs_tau = deepcopy(hole_msd_vs_time)
  ln_tau = np.log(hole_msd_vs_tau.x)
  diff_ln_tau = np.diff(ln_tau)
  diff_ln_msd = np.diff(np.log(hole_msd_vs_tau.y))
  msd_exponent = diff_ln_msd / diff_ln_tau
  props = dict(hole_msd_vs_tau.props)
  props['observation'] = 'MSD exponent vs. ln tau'
  props['xlabel'] = r'$\ln\tau$'
  props['ylabel'] = r'$\alpha$'
  return akd.MeasuData(ln_tau[:-1], msd_exponent, props)


def _get_msd(local_hole_vs_tau, idx_coor_map, L):
  ref_point = idx_coor_map[L-1]
  # ref_point[1] = 0.5
  site_num = len(idx_coor_map)
  relative_coor = idx_coor_map - np.array([ref_point]*site_num)
  relative_dis2 = []
  for idx in range(site_num):
    rel_coor_at_site = relative_coor[idx]
    relative_dis2.append(rel_coor_at_site[0]**2 +
                         rel_coor_at_site[1]**2)
  relative_dis2 = np.array(relative_dis2)
  msd = []
  for tau_idx in range(len(local_hole_vs_tau)):
    local_hole_at_tau = local_hole_vs_tau[tau_idx]
    msd.append(np.dot(local_hole_at_tau, relative_dis2))
  return np.array(msd)
