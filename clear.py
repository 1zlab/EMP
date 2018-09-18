import os


def clear_up(path):
    for i in os.listdir(path):
        if i == 'boot.py':
            continue
        try:
            os.remove(path+'/'+i)
        except:
            clear_up(path+'/'+i)
    os.rmdir(path)

if __name__ == "__main__":
    clear_up('/')