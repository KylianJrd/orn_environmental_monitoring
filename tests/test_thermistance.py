from machine import ADC, Pin
import time
import math

pin_thermistance = ADC(26)  # Utilisez le bon numéro de broche selon votre configuration
sensor_value = pin_thermistance.read_u16()


V_REF = 3.3
ADC_RANGE = 65535

Vr = V_REF * sensor_value/ ADC_RANGE

# Calcul de la résistance de la thermistance (en ohms)
R_SERIE = 10000
Rt = 10000 * Vr / (V_REF - Vr)

# Fonction pour calculer la température en kelvins à partir de la résistance de la thermistance
def calculate_temperature(resistance, R25, A, B, C, D):
    # Calcul de ln(Rt / R25)
    ln_ratio = math.log(Rt / R25)
    
    # Calcul de ln(Rt / R25) au carré
    ln_ratio_squared = ln_ratio ** 2
    
    # Calcul de ln(Rt / R25) au cube
    ln_ratio_cubed = ln_ratio ** 3
    
    # Calcul du terme à l'intérieur de la fraction
    inner_term = A + B * ln_ratio + C * ln_ratio_squared + D * ln_ratio_cubed
    
    # Calcul de la température en kelvins
    temperature_kelvin = 1 / inner_term
    
    return temperature_kelvin

# Exemple d'utilisation : supposons que la résistance de la thermistance soit de 10000 ohms
resistance_thermistance = 10000
R25 = 15000  # Résistance de la thermistance à 25°C
A = 0.001  # Valeur arbitraire pour A
B = 0.0001  # Valeur arbitraire pour B
C = 0.00001  # Valeur arbitraire pour C
D = 0.000001  # Valeur arbitraire pour D

temperature_kelvin = calculate_temperature(resistance_thermistance, R25, A, B, C, D)
temperature_celsius = temperature_kelvin - 1464
print("Température : {:.2f} °C".format(temperature_celsius))
