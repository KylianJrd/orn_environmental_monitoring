from usocket import socket
from machine import Pin, SPI
import network
import time
import json

led = Pin(25, Pin.OUT)

# W5x00 chip init
def w5x00_init(ip_addr='192.168.1.20'):
    spi = SPI(0, 2_000_000, mosi=Pin(19), miso=Pin(16), sck=Pin(18))
    nic = network.WIZNET5K(spi, Pin(17), Pin(20))  # spi,cs,reset pin
    nic.active(True)

    # None DHCP
    nic.ifconfig((ip_addr, '255.255.255.0', '192.168.1.1', '8.8.8.8'))

    # DHCP
    # nic.ifconfig('dhcp')
    print('IP address :', nic.ifconfig())

    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())
        
        
def read_sensors():
    # Simulated sensor data
    bme280_temp = 25.5
    bme280_pressure = 1013.2
    bme280_humidity = 60
    lm35_temp = 22.3
    ldr_brightness = 75
    wind_direction = 180
    wind_speed = 15.5
    rain_quantity = 10.2

    # Construct JSON object
    sensors_data = {"capteurs": [{"nom": "bme_1", "unit_humidity": "pourcentage", "values_temperature": 23.57, "active": 1, "type": "BME280", "interface": "i2c", "adresse_i2c": "0x77", "pin_analog": "None", "pin_scl": "1", "unit_pressure": "hPa", "values_humidity": 41.125, "pin_sda": "0", "unit_temperature": "degre celsius", "values_pressure": 98839.52}, {"type": "LDR", "pin_sda": "None", "interface": "analog", "adresse_i2c": "None", "pin_analog": "26", "pin_scl": "None", "active": 1, "unit_values": "pourcentage", "values": 15.45739, "nom": "ldr_1"}, {"type": "ANEMOMETER", "pin_sda": "None", "interface": "None", "adresse_i2c": "None", "pin_analog": "15", "pin_scl": "None", "active": 1, "unit_values": "km/h", "values": 10.5, "nom": "anemometre_1"}]}

    return sensors_data
    


def main():
    ip_addr = '192.168.1.20'
    w5x00_init(ip_addr=ip_addr)
    s = socket()
    s.bind((ip_addr, 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print('Connect from %s' % str(addr))
        request = conn.recv(1024)
        request = str(request)
        # print('Content = %s' % request)
        led_on = request.find('/?led=on')
        led_off = request.find('/?led=off')
        if led_on == 6:
            print("LED ON")
            led.value(1)
        if led_off == 6:
            print("LED OFF")
            led.value(0)
        sensors_data = read_sensors()
        json_data = json.dumps(sensors_data)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Connection: close\n')
        conn.send('Content-Type: application/json\n')
        conn.send('Content-Length: %s\n\n' % len(json_data))
        conn.send(json_data)
        conn.close()

if __name__ == "__main__":
    main()











