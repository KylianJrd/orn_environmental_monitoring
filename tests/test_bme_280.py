from machine import Pin, I2C
from time import sleep
from lib import bme280

# Initialize I2C communication
i2c = I2C(id=0, scl=Pin(1), sda=Pin(0), freq=400000)
print(i2c.scan())

bme = bme280.BME280(i2c=i2c,address=0x77)



print('tot')
while True:

    # Read sensor data
    values = bme.values


    # Convert temperature to fahrenheit
    #tempF = (bme.read_temperature()/100) * (9/5) + 32
    #tempF = str(round(tempF, 2)) + 'F'

    # Print sensor readings
    unite = ['Température','Pression','Humidité']
    for idx, val in enumerate(values):
        print(unite[idx],':',val)
        

    sleep(5)