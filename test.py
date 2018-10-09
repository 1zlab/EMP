from emp_wifi import Wifi

if __name__ == '__main__':
    Wifi.connect()
    import os
    if not 'webrepl_cfg.py' in os.listdir():
        import webrepl_setup
    from emp_webrepl import WebREPL
    WebREPL.start()
    from emp_dev import *