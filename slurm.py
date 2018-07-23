from __future__ import absolute_import
# 
#  Author: Rongyang Sun <sun-rongyang@outlook.com>
#  Creation Date: 2018-07-23 15:10
#  
#  Description: Extension for alpskit. Module used on Slurm cluster.
# 
import os


def change_to_loc_dir(loc_dir):
  """Change current work director to loc_dir.

  :loc_dir: str
      Local directory on a node.
  :returns: 0

  """
  if os.path.exists(loc_dir):
    os.chdir(loc_dir)
  else:
    os.makedirs(loc_dir)
    os.chdir(loc_dir)
  return 0
