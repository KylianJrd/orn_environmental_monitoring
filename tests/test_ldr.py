
from machine import Pin, I2C, ADC
import time
 
ldr = ADC(26)
 
while True:
     print((ldr.read_u16()*100)/65536)
     time.sleep(2)