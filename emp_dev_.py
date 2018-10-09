import os
import json
import gc
from emp_webrepl import WebREPL


def tree(path='/'):
    root = dict(name=path, children=[])
    index = 0
    dirs = os.listdir(path)
    for i in dirs:
        try:
            root['children'].append(
                dict(name=i, children=[dict(name=j) for j in os.listdir(i)]))
        except:
            root['children'].append(dict(name=i))

    for i in root['children']:
        if not i.get('children', False):
            i['index'] = index
            index += 1
        else:
            for j in i['children']:
                j['index'] = index
                index += 1
    rsp = dict(func='tree', data=root)
    WebREPL.send(json.dumps(rsp) + '\n\r')
    gc.collect()


def get_code(filename):
    gc.collect()
    with open(filename, 'r') as f:
        print(f.read())


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
