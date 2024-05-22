import ujson
from machine import Pin, I2C, ADC
import time
  
def charger_configuration(nom_fichier):
    with open(nom_fichier, 'r') as f:
        config = ujson.load(f)
    return config


def init_sonde_analog(pin_analog):
    # Conversion du numéro de broche analogique en entier
    pin_analog = int(pin_analog)
    return ADC(Pin(pin_analog))


# Fonction pour convertir la valeur lue en pourcentage de lumière
def convert_to_light_percentage(sensor_value, max_value=65535):
    light_percentage = (sensor_value / max_value) * 100
    return light_percentage

config = charger_configuration('config_sondes.json')

# Boucle principale
while True:
    for capteur in config['capteurs']:
        if capteur['interface'] == 'analog':
            pin_photoreceptor = init_sonde_analog(capteur['pin_analog'])
            # Lecture de la valeur de la photorésistance
            sensor_value = pin_photoreceptor.read_u16()
            # Conversion en pourcentage de lumière
            light_percentage = convert_to_light_percentage(sensor_value)
            # Affichage du pourcentage de lumière
            print("Pourcentage de lumière : {:.2f}%".format(light_percentage))
    # Attente avant la prochaine lecture
    time.sleep(1)  # Attendez 1 seconde entre chaque lecture
