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


def get_slurm_submit_dir():
  """Get SLURM_SUBMIT_DIR envirnment variable.
  :returns: str
      SLURM_SUBMIT_DIR environment variable if it is defined.
      Or ''.

  """
  return _get_env_val('SLURM_SUBMIT_DIR')


def get_slurm_jobid():
  """Get SLURM_JOBID environment variable.
  :returns: str
      SLURM_JOBID environment variable value if it is defined.
      Or ''.

  """
  return _get_env_val('SLURM_JOBID')


def cph5to(target_dir):
  """Copy ./*.h5 files to target_dir.

  :target_dir: str
      Target directory.
  :returns: os.system return

  """
  return os.system('cp ./*.h5 ' + target_dir)


def cpchkpto(target_dir):
  """Copy ./*.chkp directories to target_dir.

  :target_dir: str
      Target directory.
  :returns: os.system return

  """
  return os.system('cp -r ./*.chkp ' + target_dir)


def _get_env_val(key):
  value = os.environ.get(str(key))
  if value == None: value = ''
  return value
