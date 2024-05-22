import ujson
from machine import Pin, I2C
from time import sleep
from lib import bme280

def write_bme_values(config, bme_data):
    # Met à jour les valeurs du capteur BME280
    for capteur in config['capteurs']:
        if capteur['type'] == 'BME280':
            # Met à jour les valeurs de pression, température et humidité
            capteur['values_pressure'] = bme_data[0][1]  # Index 1 pour la pression dans bme_data
            capteur['values_temperature'] = bme_data[0][0]  # Index 0 pour la température dans bme_data
            capteur['values_humidity'] = bme_data[0][2]  # Index 2 pour l'humidité dans bme_data
            break  # Sortez de la boucle une fois que le capteur BME280 a été trouvé

    # Écrit le dictionnaire mis à jour dans le fichier de configuration
    with open('config_sondes.json', 'w') as f:
        ujson.dump(config, f)  # Écrire le fichier avec la nouvelle configuration



def init_sonde_i2c(config):
    i2c_sensors = []

    for capteur in config['capteurs']:
        if capteur['interface'] == 'i2c':
            i2c_address = int(capteur['adresse_i2c'], 16)
            i2c_scl = int(capteur['pin_scl'])
            i2c_sda = int(capteur['pin_sda'])
            i2c_sensor = bme280.BME280(i2c=I2C(id=0, scl=Pin(i2c_scl), sda=Pin(i2c_sda), freq=400000), address=i2c_address)
            i2c_sensors.append(i2c_sensor)

    return i2c_sensors

def read_sensor_data(sensor):
    return sensor.read_compensated_data()

def convert_to_unite(sensor_values):
    return [val / unit_divisor for val, unit_divisor in zip(sensor_values, [100, 256, 1024])]

def read_bme_data(config):
    i2c_sensors = init_sonde_i2c(config)
    temp, press, hum = read_sensor_data(i2c_sensors[0])
    bme_data = convert_to_unite([temp, press, hum])
    return bme_data
