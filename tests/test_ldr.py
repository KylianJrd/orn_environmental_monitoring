
from machine import Pin, I2C, ADC
import time
 
# Configuration du broche analogique pour la lecture de la photorésistance
pin_photoreceptor = ADC(27)  # Utilisez le bon numéro de broche selon votre configuration

# Fonction pour convertir la valeur lue en pourcentage de lumière
def convert_to_light_percentage(sensor_value, max_value=65535):
    light_percentage = (sensor_value / max_value) * 100
    return light_percentage

# Boucle principale
while True:
    # Lecture de la valeur de la photorésistance
    sensor_value = pin_photoreceptor.read_u16()
    
    # Conversion en pourcentage de lumière
    light_percentage = convert_to_light_percentage(sensor_value)
    
    # Affichage du pourcentage de lumière
    print("Pourcentage de lumière : {:.2f}%".format(light_percentage))
    
    # Attente avant la prochaine lecture
    time.sleep(1)  # Attendez 1 seconde entre chaque lecture