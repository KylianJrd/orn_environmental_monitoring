from machine import Pin, I2C, ADC
from time import sleep
import utime

analog_value = ADC(26)
conversion_factor = 3.3/ 65535

while True:
    temp_voltage_raw = analog_value.read_u16()
    convert_voltage = temp_voltage_raw*conversion_factor
    tempC = convert_voltage/(10.0 / 1000)
    print("Temperature: ",tempC, "°C", sep=" ")
    sleep(2)