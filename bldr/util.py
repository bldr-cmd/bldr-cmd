import errno
import os
import stat
import shutil

def rmtree(path):
    """
    A Windows-safe version of rmtree

    Windows marks .git files as readonly, making them insanely hard to delete.  

    This function is a workaround
    """
    shutil.rmtree(path, ignore_errors=False, onerror=handle_remove_readonly)


def handle_remove_readonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise