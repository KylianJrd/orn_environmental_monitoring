
from machine import Pin, I2C, ADC
import time
 
ldr = ADC(26)
 
while True:
    val = ldr.read_u16()
    print(val)
    print((val*100)/65536)
    time.sleep(2)
