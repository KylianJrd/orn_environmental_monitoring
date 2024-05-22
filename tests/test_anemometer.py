from machine import Pin
from time import sleep
from _thread import start_new_thread, allocate_lock

# Variable globale pour stocker le compteur de détection d'impulsions
compteur_impulsions = 0
integration = 2

# Fonction appelée lors de la détection d'une impulsion pour incrémenter le compteur
def detection_impulsion(p, verrou):
    global compteur_impulsions  # Référence à la variable globale
    with verrou:
        compteur_impulsions += 1  # Incrémentation du compteur de détection d'impulsions

# Fonction du thread de surveillance qui calcule la vitesse du vent toutes les 10 secondes
def surveillance_thread(verrou, fin_thread):
    global compteur_impulsions  # Référence à la variable globale
    while not fin_thread:
        with verrou:
            vitesse_vent = (compteur_impulsions * 2.4) / integration  # Calcul de la vitesse du vent en km/h
            compteur_impulsions = 0  # Réinitialisation du compteur de détection d'impulsions
        print(f'Vitesse du vent: {vitesse_vent} km/h')
        sleep(integration)  # Attente de 10 secondes avant la prochaine mesure

# Initialisation de la broche d'entrée, création d'une interruption sur front montant et lancement d'un thread de surveillance
def initialisation_capteur_vitesse_vent(numero_broche_entree):
    verrou = allocate_lock()  # Création d'un verrou pour la synchronisation des threads
    fin_thread = False  # Variable pour indiquer la fin du thread
    broche_entree = Pin(numero_broche_entree, Pin.IN, Pin.PULL_DOWN)  # Configuration de la broche d'entrée en tant que GPIO en entrée avec résistance de pull-up
    broche_entree.irq(trigger=Pin.IRQ_RISING, handler=lambda p: detection_impulsion(p, verrou))  # Définition de la fonction de traitement de l'interruption pour détecter les impulsions
    start_new_thread(surveillance_thread, (verrou, fin_thread))  # Démarrage du thread de surveillance

# Fonction principale pour tester le capteur de vitesse du vent
if __name__ == "__main__":
    try:
        initialisation_capteur_vitesse_vent(14)  # Initialisation du capteur de vitesse du vent sur la broche 0
        while True:
            sleep(1)  # Attente d'une seconde
    except KeyboardInterrupt:
        pass  # Ignorer l'exception KeyboardInterrupt et terminer proprement le programme
