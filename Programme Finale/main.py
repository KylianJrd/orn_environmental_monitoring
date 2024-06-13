import ujson
from time import sleep
from sensor import sensor_ldr, sensor_bme_280, sensor_anemometre
from usocket import socket
from machine import Pin, SPI
import network
import time
import json

def w5x00_init(ip_addr='192.168.1.20'):
    spi = SPI(0, 2_000_000, mosi=Pin(19), miso=Pin(16), sck=Pin(18))
    nic = network.WIZNET5K(spi, Pin(17), Pin(20))
    nic.active(True)
    nic.ifconfig((ip_addr, '255.255.255.0', '192.168.1.1', '8.8.8.8'))
    print('IP address :', nic.ifconfig())
    while not nic.isconnected():
        time.sleep(1)
        print(nic.regs())

def charger_configuration(nom_fichier):
    with open(nom_fichier, 'r') as f:
        config = ujson.load(f)
    return config

def read_json_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def write_json_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)

def main():
    config = charger_configuration('config_sondes.json')
    w5x00_init(ip_addr=config['ip'])
    s = socket()
    s.bind((config['ip'], 80))
    s.listen(5)

    wind_readings = []

    for sensor in config['capteurs']:
        if sensor['type'] == 'ANEMOMETER' and sensor['active']:
            sensor_anemometre.initialisation_anemometre(sensor['pin_digital'])
        elif sensor['type'] == 'WINDVANE' and sensor['active']:
            sensor_anemometre.initialisation_girouette(sensor['pin_analog'])
        elif sensor['type'] == 'PLUVIOMETER' and sensor['active']:
            sensor_anemometre.initialisation_pluviometre(sensor['pin_digital'])

    while True:
        conn, addr = s.accept()
        print('Connect from %s' % str(addr))
        request = conn.recv(1024)
        request = str(request)
        print("Request received:", request)

        refresh = request.find('GET /')

        if refresh != -1:
            print("Refreshing sensor data")

            data_json = {"ip": config['ip'],
                         "name": config['name'],
                         "groupe": config['groupe'],
                         "capteurs": []}
            print(config)
            for sensor_config in config['capteurs']:
                sensor = sensor_config.copy()
                if sensor['type'] == 'BME280' and sensor['active']:
                    try:
                        bme_data = sensor_bme_280.read_bme_data(config)
                        sensor['values'] = bme_data
                    except Exception as err:
                        sensor['error'] = str(err)
                    data_json['capteurs'].append(sensor)
                elif sensor['type'] == 'LDR' and sensor['active']:
                    try:
                        light_percentages = sensor_ldr.read_light_percentage(config)
                        sensor['values'] = light_percentages[0]
                        data_json['capteurs'].append(sensor)
                    except ValueError as e:
                        print(f"Error initializing LDR sensor: {e}")
                elif sensor['type'] == 'ANEMOMETER' and sensor['active']:
                    vitesse_vent, average_direction, pluviometrie = sensor_anemometre.measure_anemometer_data(sensor['pin_digital'], None, None, wind_readings)
                    sensor['values'] = vitesse_vent
                    data_json['capteurs'].append(sensor)
                elif sensor['type'] == 'PLUVIOMETER' and sensor['active']:
                    vitesse_vent, average_direction, pluviometrie = sensor_anemometre.measure_anemometer_data(None, None, sensor['pin_digital'], wind_readings)
                    sensor['values'] = pluviometrie
                    data_json['capteurs'].append(sensor)
                elif sensor['type'] == 'WINDVANE' and sensor['active']:
                    vitesse_vent, average_direction, _ = sensor_anemometre.measure_anemometer_data(None, sensor['pin_analog'], None, wind_readings)
                    sensor['values'] = average_direction
                    data_json['capteurs'].append(sensor)

            json_data = json.dumps(data_json)
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Connection: close\n')
            conn.send('Content-Type: application/json\n')
            conn.send('Content-Length: %s\n\n' % len(json_data))
            conn.send(json_data)
            conn.close()
            continue

        json_data = json.dumps(data_json)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Connection: close\n')
        conn.send('Content-Type: application/json\n')
        conn.send('Content-Length: %s\n\n' % len(json_data))
        conn.send(json_data)
        conn.close()

if __name__ == "__main__":
    main()








