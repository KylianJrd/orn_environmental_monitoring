from machine import Pin, ADC
import math
import utime

# Variables globales pour stocker les compteurs de détection d'impulsions
compteur_impulsions_anemometre = 0
compteur_impulsions_pluviometre = 0
integration_anemometre = 2
integration_pluviometre = 2

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

# Fonction appelée lors de la détection d'une impulsion pour incrémenter le compteur (anemometre et pluviometre)
def detection_impulsion(p, type_capteur):
    global compteur_impulsions_anemometre, compteur_impulsions_pluviometre
    if type_capteur == "anemometre":
        compteur_impulsions_anemometre += 1
    elif type_capteur == "pluviometre":
        compteur_impulsions_pluviometre += 1

# Initialisation des broches d'entrée pour les capteurs
def initialisation_capteurs(numero_broche_anemometre, numero_broche_pluviometre):
    broche_anemometre = Pin(numero_broche_anemometre, Pin.IN, Pin.PULL_DOWN)  # Configuration de la broche d'entrée pour l'anemometre
    broche_anemometre.irq(trigger=Pin.IRQ_RISING, handler=lambda p: detection_impulsion(p, "anemometre"))  # Définition de la fonction de traitement de l'interruption pour détecter les impulsions de l'anemometre

    broche_pluviometre = Pin(numero_broche_pluviometre, Pin.IN, Pin.PULL_UP)  # Configuration de la broche d'entrée pour le pluviometre
    broche_pluviometre.irq(trigger=Pin.IRQ_RISING, handler=lambda p: detection_impulsion(p, "pluviometre"))  # Définition de la fonction de traitement de l'interruption pour détecter les impulsions du pluviometre

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

# Fonction principale pour initialiser et tester les capteurs
if __name__ == "__main__":
    try:
        initialisation_capteurs(15, 16)  # Initialisation des capteurs (broche 0 pour l'anemometre et 16 pour le pluviometre)
        wind_readings = []
        while True:
            # Surveillance de l'anemometre et du pluviometre
            utime.sleep(max(integration_anemometre, integration_pluviometre))
            # Lecture de la valeur ADC pour l'anemometre
            u2 = adc.read_u16() * conversion_factor
            # Calcul de la résistance de la girouette
            R2 = (-u2 * 9940) / (u2 - 3.3)
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
            # Calculer la direction moyenne du vent
            average_direction = calculate_average_wind_direction(wind_readings)
            # Calculer la vitesse du vent
            vitesse_vent = (compteur_impulsions_anemometre * 2.4) / integration_anemometre  # Calcul de la vitesse du vent en km/h
            # Calculer la pluviométrie
            pluviometrie = compteur_impulsions_pluviometre * 0.2794  # Calcul de la pluviométrie en mm
            # Afficher les valeurs
            print(f'Direction moyenne du vent: {average_direction} degrés - Vitesse du vent: {vitesse_vent} km/h - Pluviométrie: {pluviometrie} mm')
            compteur_impulsions_anemometre = 0
            compteur_impulsions_pluviometre = 0

    except KeyboardInterrupt:
        pass  # Ignorer l'exception KeyboardInterrupt et terminer proprement le programme





