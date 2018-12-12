from machine import PWM
from machine import Pin
from machine import Timer
from machine import ADC
import utime, math


dac = DAC(Pin(26,Pin.OUT), bits=12)
pwm = PWM(Pin(27),freq=1000)


def pulse(dac, period, gears):
    """呼吸灯函数
    
    Arguments:
        dac {[DAC]} -- [DAC对象]
        period {[type]} -- [周期]
        gears {[type]} -- [亮度档位]
    """


    for i in range(2 * gears):
        dac.write(int(math.sin(i / gears * math.pi) * 2000) + 2048)
        pwm.duty(int(math.sin(i / gears * math.pi) * 500) + 523)
        # 延时
        utime.sleep_ms(int(period / (2 * gears)))

# 呼吸十次
for i in range(10):
    pulse(dac, 2000, 100)




for i in dir(machine):
    print('%s ==> %s' % (i, getattr(machine, i)))
