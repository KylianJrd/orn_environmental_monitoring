import ujson
from machine import Pin, ADC
import math

conversion_factor = 3.3 / 65535
compteur_impulsions_anemometre = 0

wind_vane_data = {
    33000: 0.0, 9500: 22.5, 11000: 45.0, 3140: 67.5, 3400: 90.0, 
    1400: 112.5, 2200: 135.0, 600: 157.5, 1000: 180.0, 900: 202.5, 
    6200: 225.0, 17120: 247.5, 13000: 270.0, 25000: 292.5, 64900: 315.0, 
    21880: 337.5
}

R1 = 9940  # Résistance fixe

def detection_impulsion(p):
    global compteur_impulsions_anemometre
    compteur_impulsions_anemometre += 1

def initialisation_anemometre(pin_anemometre):
    try:
        pin = int(pin_anemometre)
        return Pin(pin, Pin.IN, Pin.PULL_DOWN)
    except ValueError:
        raise ValueError(f"Invalid pin_digital value: {pin_anemometre}")

def initialisation_girouette(pin_analog):
    try:
        pin = int(pin_analog)
        return ADC(Pin(pin))
    except ValueError:
        raise ValueError(f"Invalid pin_analog value: {pin_analog}")

def calculate_average_wind_direction(wind_readings):
    if not wind_readings:
        return 0.0

    sin_sum = sum(math.sin(math.radians(angle)) for angle in wind_readings)
    cos_sum = sum(math.cos(math.radians(angle)) for angle in wind_readings)

    average = math.degrees(math.atan2(sin_sum, cos_sum))
    return (average + 360) % 360

def measure_anemometer_data(pin_anemometre, pin_girouette, wind_readings):
    if pin_anemometre is not None:
        broche_anemometre = initialisation_anemometre(pin_anemometre)
        broche_anemometre.irq(trigger=Pin.IRQ_RISING, handler=detection_impulsion)

    vitesse_vent = (compteur_impulsions_anemometre * 2.4) / 2  # Ajuster l'intervalle d'intégration selon votre configuration

    if pin_girouette is not None:
        adc = initialisation_girouette(pin_girouette)
        u2 = adc.read_u16() * conversion_factor

        if u2 == 3.3:
            print("Warning: u2 is 3.3, skipping R2 calculation to avoid division by zero.")
            return vitesse_vent, calculate_average_wind_direction(wind_readings)

        R2 = (-u2 * R1) / (u2 - 3.3)

        angle_correspondant = min(wind_vane_data, key=lambda r: abs(r - R2))
        wind_readings.append(wind_vane_data[angle_correspondant])
        if len(wind_readings) > 10:
            wind_readings.pop(0)

        average_direction = calculate_average_wind_direction(wind_readings)

        return vitesse_vent, average_direction
    else:
        return vitesse_vent, None











