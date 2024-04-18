from lib import machine
from time import sleep



sensor = machine.ADC(26)

while True:
    valeur = sensor.read_u16() * 3.3 / 65535
    temperature = (valeur - 0.5) * 100
    print("Température : {:.1f}°C".format(temperature))
    time.sleep(1)