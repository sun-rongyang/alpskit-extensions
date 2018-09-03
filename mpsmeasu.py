from __future__ import absolute_import
# 
#  Author: Rongyang Sun <sun-rongyang@outlook.com>
#  Creation Date: 2018-07-10 16:51
#  
#  Description: Extension for alpskit. MPS simulation measurement.
# 
import alpskit.data as akd
from . import squarelattice as sl
from . import chainlattice as cl

from copy import deepcopy

import numpy as np


def measu_hole_msd_vs_time(case_data, lattice='square lattice'):
  """Measure hole MSD (<r^2>) vs. time. Just for ONE hole case. 

  :case_data: str
      Data folder to contain the data JSON files for the case.
  :returns: alpskit.data.MeasuData
      MSD vs. time data.

  """
  def _get_idx_coor_map_and_lattice_size(data, lattice):
    if lattice == 'chain lattice':
      lattice_size = {'name': lattice,
                      'L': int(data.props['L'])}
      idx_coor_map = cl.get_idx_coor_map(lattice_size['L']) 
    elif lattice == 'square lattice':
      lattice_size = {'name': lattice,
                      'L': int(data.props['L']),
                      'W': int(data.props['W'])}
      idx_coor_map = sl.get_idx_coor_map(lattice_size['L'],
                                         lattice_size['W'])
    return (idx_coor_map, lattice_size)

  orig_data_file_name = 'local_n_vs_tau.json'
  local_n_vs_tau = akd.js_to_measu_data(case_data +'/'+ orig_data_file_name)
  idx_coor_map, lattice_size = \
      _get_idx_coor_map_and_lattice_size(local_n_vs_tau, lattice)
  local_hole_vs_tau_data = 1 - local_n_vs_tau.y
  msd = _get_msd(local_hole_vs_tau_data, idx_coor_map, lattice_size)
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


def measu_entropy_vs_time(case_data, cut_bond):
  """Measure entanglement entropy at `cut_bond' vs. time.

  :case_data: str
      Data folder to contain the data JSON files for the case.
  :cut_bond: int
      index of the cut bond start from 0.
  :returns: alpskit.data.MeasuData
      Entropy vs. time data.

  """
  orig_data_file_name = 'entropy_vs_tau.json'
  entropy_vs_tau = akd.js_to_measu_data(case_data+'/'+orig_data_file_name)
  tau = np.array(entropy_vs_tau.x)
  entropy = entropy_vs_tau.y[:,cut_bond]
  props = dict(entropy_vs_tau.props)
  props['observation'] = 'Entropy vs. time'
  props['xlabel'] = r'$\tau$'
  props['ylabel'] = r'EE'
  return akd.MeasuData(tau, entropy, props)

def _get_msd(local_hole_vs_tau, idx_coor_map, lattice_size):
  if lattice_size['name'] == 'chain lattice':
    ref_point = idx_coor_map[int(lattice_size['L']/2)]
  elif lattice_size['name'] == 'square lattice':
    ref_point = idx_coor_map[lattice_size['L']-1]
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
