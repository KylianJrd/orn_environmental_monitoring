from lib.sht31 import SHT31
from lib import bme280
from machine import Pin, I2C, ADC
from time import sleep_ms
import utime
import dht
import math

# Fonction pour convertir la valeur lue en pourcentage de lumière
def convert_to_light_percentage(sensor_value, max_value=65535):
    light_percentage = (sensor_value / max_value) * 100
    return light_percentage

# Variables globales pour stocker les compteurs de détection d'impulsions
compteur_impulsions_anemometre = 0
compteur_impulsions_pluviometre = 0
integration_anemometre = 2
integration_pluviometre = 2

# Configuration des broches d'entrée pour les capteurs
def initialisation_capteurs(numero_broche_anemometre, numero_broche_pluviometre):
    broche_anemometre = Pin(numero_broche_anemometre, Pin.IN, Pin.PULL_DOWN)
    broche_anemometre.irq(trigger=Pin.IRQ_RISING, handler=lambda p: detection_impulsion(p, "anemometre"))

    broche_pluviometre = Pin(numero_broche_pluviometre, Pin.IN, Pin.PULL_UP)
    broche_pluviometre.irq(trigger=Pin.IRQ_RISING, handler=lambda p: detection_impulsion(p, "pluviometre"))

# Fonction pour calculer la direction moyenne du vent
def calculate_average_wind_direction(wind_readings):
    reading_count = len(wind_readings)
    if reading_count == 0:
        return 0.0

    sin_sum = 0.0
    cos_sum = 0.0

    for angle in wind_readings:
        radians = math.radians(angle)
        sin_sum += math.sin(radians)
        cos_sum += math.cos(radians)

    sin_average = sin_sum / reading_count
    cos_average = cos_sum / reading_count

    arc = math.degrees(math.atan2(sin_average, cos_average))
    average = (arc + 360) % 360

    return average

# Fonction appelée lors de la détection d'une impulsion pour incrémenter le compteur
def detection_impulsion(p, type_capteur):
    global compteur_impulsions_anemometre, compteur_impulsions_pluviometre
    if type_capteur == "anemometre":
        compteur_impulsions_anemometre += 1
    elif type_capteur == "pluviometre":
        compteur_impulsions_pluviometre += 1

# Configuration du port I2C
i2c = I2C(id=0, scl=Pin(1), sda=Pin(0), freq=400000)
print(i2c.scan())

# Initialisation des capteurs BME280 et SHT31
bme = bme280.BME280(i2c=i2c, address=0x77)
sht = SHT31(i2c=i2c)

# Configuration de la broche analogique pour la photorésistance
pin_photoreceptor = ADC(27)

# Configuration du capteur LM35
analog_value = ADC(28)
conversion_factor = 3.3 / 65535

# Configuration du capteur DHT11
# capteur = dht.DHT11(Pin(5))

# Initialisation des broches pour les capteurs de vent et de pluie
initialisation_capteurs(15, 16)

# Initialisation des variables pour la direction du vent
wind_vane_data = {
    33000: 0.0,
    9500: 22.5,
    11000: 45.0,
    3140: 67.5,
    3400: 90.0,
    1400: 112.5,
    2200: 135.0,
    600: 157.5,
    1000: 180.0,
    900: 202.5,
    6200: 225.0,
    17120: 247.5,
    13000: 270.0,
    25000: 292.5,
    64900 : 315.0,
    21880 : 337.5
}  # Compléter avec les données de la girouette
adc = ADC(26)
conversion_factor = 3.3 / 65535
wind_readings = []


time = 1714052965

# Ouvrir le fichier CSV en mode ajout
with open("mesures7capteurs.csv", "w+") as log:
    chaine = "timestamp,c_sht,h_sht,c_bme,p_bme,h_bme,c_lm,lux_diode,direction_vent,vitesse_vent,pluviometrie\n"
    log.write(chaine)
    print(chaine)
    while True:
        # Temporisation d'une seconde
        sleep_ms(10000)
        time += 10

        # Obtenir les données de température et d'humidité
        shtdata = sht.get_temp_humi()
        bme_values = bme.values

        # Lecture de la valeur ADC pour la photorésistance
        sensor_value = pin_photoreceptor.read_u16()
        light_percentage = convert_to_light_percentage(sensor_value)

        # Lecture de la valeur ADC pour le LM35
        temp_voltage_raw = analog_value.read_u16()
        convert_voltage = temp_voltage_raw * conversion_factor
        tempC = convert_voltage / (10.0 / 1000)

        # Lecture de la valeur ADC pour l'anemometre
        u2 = adc.read_u16() * conversion_factor
        R2 = (-u2 * 9940) / (u2 - 3.3)
        delta_min = 1000000
        angle_correspondant = None
        for resistance, angle in wind_vane_data.items():
            delta = abs(resistance - R2)
            if delta < delta_min:
                delta_min = delta
                angle_correspondant = angle
        wind_readings.append(angle_correspondant)
        if len(wind_readings) > 10:
            wind_readings.pop(0)
        average_direction = calculate_average_wind_direction(wind_readings)
        vitesse_vent = (compteur_impulsions_anemometre * 2.4) / integration_anemometre
        pluviometrie = compteur_impulsions_pluviometre * 0.2794

        # Enregistrement des mesures dans le fichier CSV
        chaine = "{},{},{},{},{},{},{},{},{},{},{}\n".format(time, *shtdata, *bme_values, tempC, light_percentage, average_direction, vitesse_vent, pluviometrie)
        log.write(chaine)
        print(chaine)
        log.flush()


 