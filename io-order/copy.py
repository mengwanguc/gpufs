




import os
import sys

import shutil, errno
import time

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)
        else: raise

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


directory = sys.argv[1]
classes = [d.name for d in os.scandir(directory) if d.is_dir() and d.name[0] == 'n']

directory_size = get_size(directory)

while directory_size < 1024 * 1024 * 1024 * 50:
    for c in classes:
        copy_folder_name = directory+"/copy_{}_{}".format(c, int(time.time()))
        copyanything(directory+c, copy_folder_name)
        directory_size += get_size(copy_folder_name)
    
