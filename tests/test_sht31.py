from machine import I2C, Pin

from time import sleep_ms
from lib.sht31 import SHT31

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur
i2c = I2C(id=0, scl=Pin(1), sda=Pin(0), freq=400000)

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

# Liste des adresses I2C des périphériques présents
print("Adresses I2C utilisées : " + str(i2c.scan()))

# Instanciation du capteur
sht = SHT31(i2c=i2c)

while True:

	# Temporisation d'une seconde
	sleep_ms(1000)
	
	# Lecture des valeurs mesurées
	shtdata = sht.get_temp_humi()

	# Affichage formatté des mesures
	print('=' * 40) # Imprime une ligne de séparation
	
	# Affiche la température en degrés Celsius.
	print("Temperature : %.1f degree celsius" %shtdata[0])
	
	# Affiche l'humidité en pourcents. 
	# Attention, le caractère '%' à la fin est dédoublé pour ne pas être interprété
	# comme une instruction de formattage !
	print("Humiditerelative : %.1f %%" %shtdata[1])