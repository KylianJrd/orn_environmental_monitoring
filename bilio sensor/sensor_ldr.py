import ujson
from machine import Pin, I2C, ADC
import time
        
def init_sonde_analog(pin_analog):
    # Conversion du numéro de broche analogique en entier
    pin_analog = int(pin_analog)
    return ADC(Pin(pin_analog))

# Fonction pour convertir la valeur lue en pourcentage de lumière
def convert_to_light_percentage(sensor_value, max_value=65535):
    light_percentage = (sensor_value / max_value) * 100
    return light_percentage


def read_light_percentage(config):
    light_percentages = []
    for capteur in config['capteurs']:
        if capteur['interface'] == 'analog':
            pin_photoreceptor = init_sonde_analog(capteur['pin_analog'])
            sensor_value = pin_photoreceptor.read_u16()
            light_percentage = convert_to_light_percentage(sensor_value)
            light_percentages.append(light_percentage)
    return light_percentages