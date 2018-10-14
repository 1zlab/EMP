import os
import json
import gc
from emp_webrepl import emp_sender
from emp_utils import is_folder
from emp_utils import traverse

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
        return dict(code=f.read(), filename=filename)
              
def create_folder(folder):
    try:
        os.mkdir(folder)
    except:
        pass
    tree()

def new_file(filename):
    with open(filename, 'w') as f:
        print(f.write(''))
    tree()

def del_folder(folder):
    for i in os.listdir(folder):
        os.remove(folder + '/' + i)
    os.rmdir(folder)
    tree()

def del_file(filename):
    os.remove(filename)
    tree()
