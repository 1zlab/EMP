import os
import json
import gc
import sys
from emp_webrepl import emp_sender
from emp_utils import is_folder
from emp_utils import traverse


@emp_sender
def device_info():
    return dict(
        platform=sys.platform,
        version=sys.version,
        implementation=[sys.implementation[0], list(sys.implementation[1])],
        maxsize=sys.maxsize / 1024 / 1024)


@emp_sender
def memory_status():
    gc.collect()
    return dict(alloced=gc.mem_alloc() / 1024, free=gc.mem_free() / 1024)


@emp_sender
def memory_analysing(filename):
    gc.collect()
    fsize = os.stat(filename)[6]
    mf = gc.mem_free()
    return dict(fsize=fsize, mf=mf, filename=filename)


@emp_sender
def tree(path='/'):
    return traverse(path)


@emp_sender
def get_code(filename):
    gc.collect()
    with open(filename, 'r') as f:
        code = f.read()
        rsp = dict(code=code, filename=filename)
        memory_status()
        return rsp


def new_folder(folder):
    try:
        os.mkdir(folder)
    except:
        pass
    tree()


def new_file(filename):
    with open(filename, 'w') as f:
        print(f.write(''))
    tree()


def del_folder(path):
    for i in os.listdir(path):
        if is_folder(path + '/' + i):
            del_folder(path + '/' + i)
        else:
            os.remove(path + '/' + i)

    os.rmdir(path)
    tree()


def del_file(filename):
    os.remove(filename)
    tree()


def rename(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        tree()
    except:
        pass


def emp_install(pkg):
    try:
        upip.install(pkg)
    except:
        import upip
        upip.install(pkg)

