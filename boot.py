from boot_config import *
from emp_wifi import Wifi
from emp_webrepl import WebREPL
from emp_utils import webrepl_pass
from emp_utils import post_ip
from emp_utils import is_folder    
from emp_utils import rainbow
import os

def boot():
    """配置启动模式
    """
    if enable_wifi == True:
        # print(rainbow(''))
        Wifi.connect()
        if allow_post_ip == True:
            post_ip(Wifi.ifconfig()[0][0])

    if enable_repl == True:
        WebREPL.start(password=webrepl_pass())

    if scripts is not None and  os.path.exists(scripts) and not is_folder(scripts):
        exec(open(scripts).read(),globals())