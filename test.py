from emp_wifi import Wifi
from emp_wifi import WifiHelper

if __name__ == '__main__':
    wifi = Wifi()
    WifiHelper.auto_connect(wifi)
    import os
    if not 'webrepl_cfg.py' in os.listdir():
        import webrepl_setup
    import webrepl
    webrepl.start()
