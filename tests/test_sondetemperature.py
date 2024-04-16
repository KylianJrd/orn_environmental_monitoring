import machine
import onewire
import ds18x20
import time

# Configure le pin GPIO pour le bus 1-Wire
ow = onewire.OneWire(machine.Pin(26))

# Crée un objet DS18X20
temp_sensor = ds18x20.DS18X20(ow)

# Recherche des capteurs DS18B20
roms = temp_sensor.scan()

# Vérifie s'il y a au moins un capteur DS18B20
if len(roms) == 0:
    print("Aucun capteur DS18B20 trouvé !")
    raise SystemExit

# Boucle de lecture de la température
while True:
    # Lance la conversion de température sur tous les capteurs
    temp_sensor.convert_temp()

    # Attends que la conversion soit terminée
    time.sleep_ms(750)

    # Lit la température pour chaque capteur
    for rom in roms:
        temp = temp_sensor.read_temp(rom)
        print(f"Température du capteur : {temp} °C")

    # Attends un certain temps avant de relire la température
    time.sleep(2)
