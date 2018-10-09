import os
import json
import gc
from emp_webrepl import WebREPL


def depends_on_memory(filename):
    gc.collect()
    fsize = os.stat(filename)[6]
    mf = gc.mem_free()
    rsp = dict(func='depends_on_memory', fsize=fsize, mf=mf, filename=filename)
    WebREPL.send(json.dumps(rsp) + '\n\r')
    gc.collect()


def is_folder(path):
    try:
        os.listdir(path)
        return True
    except:
        return False


def node(path):
    n = dict(name=path, children=[])
    for i in os.listdir(path):
        if is_folder(path + '/' + i):
            n['children'].append(node(path + '/' + i))
        else:
            n['children'].append(dict(name=i))
    return n


def tree(path='/'):
    rsp = dict(func='tree', data=node('/'))
    WebREPL.send(json.dumps(rsp) + '\n\r')
    gc.collect()


def get_code(filename):
    gc.collect()
    with open(filename, 'r') as f:
        rsp = dict(
            func='get_code', data=dict(code=f.read(), filename=filename))
        WebREPL.send(json.dumps(rsp) + '\n\r')
        # print(f.read())


def update_code(filename, content):
    gc.collect()
    with open(filename, 'w') as f:
        print(f.write(content))


def create_folder(folder):
    try:
        os.mkdir(folder)
    except:
        pass
    tree()


def new_file(filename):
    update_code(filename, '')
    tree()


def del_folder(folder):
    for i in os.listdir(folder):
        os.remove(folder + '/' + i)
    os.rmdir(folder)
    tree()


def del_file(filename):
    os.remove(filename)
    tree()
