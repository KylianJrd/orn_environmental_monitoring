from machine import ADC
import math
from time import sleep

# Configuration du port ADC
adc = ADC(26)  # Utilisez le numéro de la broche ADC appropriée
conversion_factor = 3.3 / 65535  # Conversion de la valeur ADC en tension

# Tableau des valeurs de résistance et de l'angle correspondant
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
}

R1 = 9940  # Résistance fixe
u = 3.3  # Tension d'alimentation

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
    average = (arc + 360) % 360  # Convertir l'angle en degrés entre 0 et 360

    return average

wind_readings = []

while True:
    # Lecture de la valeur ADC
    u2 = adc.read_u16() * conversion_factor
    # Calcul de la résistance de la girouette
    R2 = (-u2 * R1) / (u2 - u)
    # Initialisation de la différence minimale et de l'angle correspondant
    delta_min = 1000000
    angle_correspondant = None
    # Recherche de l'angle correspondant dans le tableau des données de la girouette
    for resistance, angle in wind_vane_data.items():
        delta = abs(resistance - R2)
        if delta < delta_min:
            delta_min = delta
            angle_correspondant = angle
    # Ajouter l'angle mesuré à la liste des lectures du vent
    wind_readings.append(angle_correspondant)
    # Limiter la liste des lectures du vent à 10 éléments
    if len(wind_readings) > 10:
        wind_readings.pop(0)
    # Calculer et afficher la direction moyenne du vent
    average_direction = calculate_average_wind_direction(wind_readings)
    print("Direction moyenne du vent:", average_direction)
    sleep(0.3)



