from machine import Pin, I2C, ADC
from time import sleep
import dht

capteur = dht.DHT11(Pin(5))

while True:
    try:
        sleep(1)
        # Le DHT11 renvoie au maximum une mesure toute les 1s
        capteur.measure()
        # Récupère les mesures du capteur
        print(f"Temperature : {capteur.temperature():.1f}")
        print(f"Humidite    : {capteur.humidity():.1f}")
        # Transmet la température sur la console de l'ordinateur
    except OSError as e:
        print('Echec reception')
        # Si la pico ne reçoit pas les mesures du capteur