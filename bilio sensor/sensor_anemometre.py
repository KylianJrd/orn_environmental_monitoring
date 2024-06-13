import ujson
from machine import Pin, ADC
import math

conversion_factor = 3.3 / 65535
compteur_impulsions_anemometre = 0
compteur_impulsions_pluviometre = 0

wind_vane_data = {
    33000: 0.0, 6570: 22.5, 8200: 45.0, 891: 67.5, 1000: 90.0, 
    688: 112.5, 2200: 135.0, 1410: 157.5, 3900: 180.0, 3140: 202.5, 
    16000: 225.0, 14120: 247.5, 120000: 270.0, 42120: 292.5, 64900: 315.0, 
    21880: 337.5
}

R1 = 9940  # Résistance fixe

def detection_impulsion(p, type_capteur):
    global compteur_impulsions_anemometre, compteur_impulsions_pluviometre
    if type_capteur == "anemometre":
        compteur_impulsions_anemometre += 1
    elif type_capteur == "pluviometre":
        compteur_impulsions_pluviometre += 1

def initialisation_anemometre(pin_anemometre):
    try:
        pin = int(pin_anemometre)
        broche = Pin(pin, Pin.IN, Pin.PULL_UP)
        broche.irq(trigger=Pin.IRQ_RISING, handler=lambda p: detection_impulsion(p, "anemometre"))
        return broche
    except ValueError:
        raise ValueError(f"Invalid pin_digital value: {pin_anemometre}")

def initialisation_girouette(pin_analog):
    try:
        pin = int(pin_analog)
        return ADC(Pin(pin))
    except ValueError:
        raise ValueError(f"Invalid pin_analog value: {pin_analog}")
    
def initialisation_pluviometre(pin_pluviometre):
    try:
        pin2 = int(pin_pluviometre)
        broche = Pin(pin2, Pin.IN, Pin.PULL_UP)
        broche.irq(trigger=Pin.IRQ_RISING, handler=lambda p: detection_impulsion(p, "pluviometre"))
        return broche
    except ValueError:
        raise ValueError(f"Invalid pin_digital value: {pin_pluviometre}")

def calculate_average_wind_direction(wind_readings):
    if not wind_readings:
        return 0.0

    sin_sum = sum(math.sin(math.radians(angle)) for angle in wind_readings)
    cos_sum = sum(math.cos(math.radians(angle)) for angle in wind_readings)

    average = math.degrees(math.atan2(sin_sum, cos_sum))
    return (average + 360) % 360

def measure_anemometer_data(pin_anemometre, pin_girouette, pin_pluviometre, wind_readings):
    global compteur_impulsions_anemometre, compteur_impulsions_pluviometre

    vitesse_vent = 0
    pluviometrie = 0
    average_direction = None

    if pin_anemometre is not None:
        initialisation_anemometre(pin_anemometre)
        # Calculer la vitesse du vent
        vitesse_vent = (compteur_impulsions_anemometre * 2.4) / 2  # Ajuster l'intervalle d'intégration selon votre configuration
        compteur_impulsions_anemometre = 0  # Réinitialiser le compteur après le calcul

    if pin_pluviometre is not None:
        initialisation_pluviometre(pin_pluviometre)
        # Calculer la pluviométrie
        pluviometrie = compteur_impulsions_pluviometre * 0.2794  # Calcul de la pluviométrie en mm
        compteur_impulsions_pluviometre = 0  # Réinitialiser le compteur après le calcul

    if pin_girouette is not None:
        adc = initialisation_girouette(pin_girouette)
        u2 = adc.read_u16() * conversion_factor

        if u2 == 3.3:
            print("Warning: u2 is 3.3, skipping R2 calculation to avoid division by zero.")
            return vitesse_vent, calculate_average_wind_direction(wind_readings), pluviometrie

        R2 = (-u2 * R1) / (u2 - 3.3)

        angle_correspondant = min(wind_vane_data, key=lambda r: abs(r - R2))
        wind_readings.append(wind_vane_data[angle_correspondant])
        if len(wind_readings) > 2:
            wind_readings.pop(0)

        average_direction = calculate_average_wind_direction(wind_readings)

    return vitesse_vent, average_direction, pluviometrie













