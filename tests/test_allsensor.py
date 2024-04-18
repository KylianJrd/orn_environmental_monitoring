from lib.sht31 import SHT31
from lib import bme280
from machine import Pin, I2C
from time import sleep_ms

i2c = I2C(id=0, scl=Pin(1), sda=Pin(0), freq=400000)
print(i2c.scan())

bme = bme280.BME280(i2c=i2c, address=0x77)
sht = SHT31(i2c=i2c)

time = 1713365427

# Ouvrir le fichier CSV en mode ajout

with open("mesures.csv", "w+") as log:
    chaine = "c_dht,h_dht,c_bme,p_bme,h_bme\n"
    log.write(chaine)
    print(chaine)
    while True:
        # Temporisation d'une seconde
        sleep_ms(10000)
        time += 10

        # Obtenir les données de température et d'humidité
        shtdata = sht.get_temp_humi()
        bme_values = bme.values

        # Obtenir le temps actuel au format souhaité
        #current_time = strftime("%Y-%m-%d %H:%M:%S")

        # Écrire les données dans le fichier CSV
        
        chaine = "{0},{1},{2},{3},{4},{5}\n".format(time, *shtdata,*bme_values)
        log.write(chaine)
        print(chaine)
        # Si nécessaire, vous pouvez ajouter les autres valeurs du capteur BME280 comme suit :
        # log.write("{0},{1},{2},{3},{4}\n".format(current_time, shtdata[0], shtdata[1], bme_values.temperature, bme_values.pressure))

        # Vider le tampon d'écriture pour s'assurer que les données sont écrites immédiatement
        log.flush()

