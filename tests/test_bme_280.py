from machine import Pin, I2C
from time import sleep
from lib import bme280

# Initialize I2C communication
i2c = I2C(id=0, scl=Pin(1), sda=Pin(0), freq=400000)
devices = i2c.scan()
print("I2C devices found:", devices)

# Verify if the BME280 sensor is detected
if 0x77 not in devices:
    raise Exception("BME280 sensor not found. Check connections and address.")

# Initialize the BME280 sensor
bme = bme280.BME280(i2c=i2c, address=0x77)

print('Initialization complete. Entering main loop.')

while True:
    try:
        # Read sensor data
        values = bme.values

        # Print sensor readings
        unite = ['Température', 'Pression', 'Humidité']
        for idx, val in enumerate(values):
            print(unite[idx], ':', val)
        
        sleep(5)
    except OSError as e:
        print("Error reading from sensor:", e)
        sleep(5)
