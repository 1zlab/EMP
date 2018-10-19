from emp_utils import rainbow
from emp_utils import print_as_a_list_item
from emp_utils import selection
from emp_utils import _const
from emp_utils import config_path
import os
import machine

BOOT_MODE = _const()
BOOT_MODE.WITH_NOTHING = 0
BOOT_MODE.WITH_WIFI_STARTUP = 1
BOOT_MODE.EASY_DEVELOP = 2

BOOT_MODE.WITH_WIFI_STARTUP_CODE = '''from emp_wifi import Wifi

if __name__ == '__main__':
    Wifi.connect()'''

BOOT_MODE.EASY_DEVELOP_CODE = '''from emp_wifi import Wifi
from emp_webrepl import WebREPL
from emp_utils import webrepl_pass
from emp_utils import post_ip

if __name__ == '__main__':
    Wifi.connect()
    post_ip(Wifi.ifconfig()[0][0])
    WebREPL.start(password=webrepl_pass())
    from emp_ide import *'''


def reboot():
    print(rainbow('Reboot', color='red'))
    machine.reset()


def set_boot_mode():

    print(
        print_as_a_list_item(
            0, 'Boot with nothing',
            'attention: this option will clear up boot.py, careful!'))
    print(
        print_as_a_list_item(
            1, 'Boot with wifi startup',
            'this mode will auto start wifi connect program.'))
    print(
        print_as_a_list_item(
            2, 'Easy to develop',
            'this mode is for developers.In this mode you can develop much easier via EMP-IDE(emp.1zlab.com)'
        ))

    mode = selection('Please input your choice [0-2]: ', 2)

    with open('boot.py', 'w') as f:
        if mode == BOOT_MODE.WITH_NOTHING:
            boot_code = ''
            f.write(boot_code)
            print(rainbow('Boot mode set to WITH_NOTHING', color='green'))
        elif mode == BOOT_MODE.WITH_WIFI_STARTUP:
            boot_code = BOOT_MODE.WITH_WIFI_STARTUP_CODE
            f.write(boot_code)
            print(rainbow('Boot mode set to WITH_WIFI_STARTUP', color='green'))

        elif mode == BOOT_MODE.EASY_DEVELOP:
            config_path()
            if not 'webrepl.pass' in os.listdir('config'):
                with open('config/webrepl.pass', 'w') as c:
                    c.write('1zlab')
            boot_code = BOOT_MODE.EASY_DEVELOP_CODE
            f.write(boot_code)
            print(rainbow('Boot mode set to EASY_DEVELOP', color='green'))

    reboot()