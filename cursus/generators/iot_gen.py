"""Générateur Internet des objets : MicroPython/ESP32 simulés, capteurs, MQTT.

Tout se fait sur simulateurs gratuits (Tinkercad Circuits, simulateur ESP32,
Mosquitto local) — aucun matériel requis.
"""

import random

from .base import contraintes, criteres, difficulte, duree, slug_unique

LIEUX = [
    ("serre municipale", "l'arrosage automatique", "capteur d'humidité du sol"),
    ("entrepôt frigorifique", "la chaîne du froid", "sonde de température"),
    ("parking d'immeuble", "la surveillance du niveau d'eau", "capteur ultrasonique"),
    ("élevage avicole", "le contrôle d'ambiance", "capteur température + humidité"),
    ("atelier de fabrication", "les coupures de courant", "capteur de tension"),
    ("résidence étudiante", "l'occupation des places", "capteur de mouvement PIR"),
    ("vignoble", "le gel printanier", "sonde extérieure"),
    ("piscine municipale", "le niveau et la turbidité", "capteurs de cuve"),
    ("local serveur", "l'alerte surchauffe", "sonde CTN"),
    ("ferme urbaine", "l'éclairage des bacs", "capteur de luminosité"),
    ("colis-logistique", "le suivi de choc", "accéléromètre"),
    ("station météo scolaire", "l'acquisition continue", "capteurs intégrés"),
]

CAPTEURS = ["DHT22 (temp/hum)", "BMP280 (pression)", "LDR (lumière)", "capteur ultrason HC-SR04",
            "PIR (mouvement)", "sonde CTN", "accéléromètre MPU6050", "capteur de fumée MQ-2"]
ACTIONNEURS = ["relais d'arrosage", "ventilateur", "buzzer", "LED de statut", "servomoteur de trappe", "pompe doseuse"]
BOITIERS = ["simulateur ESP32 (en ligne)", "Tinkercad Circuits", "MicroPython sur carte virtuelle", "Raspberry Pi Pico simulé"]


FAMILLES = [
    {
        "id": "capteur", "nom": "Lecture capteur", "apps": "interroger un capteur, fiabiliser la mesure et l'afficher.",
        "taches": [
            ("Lire et afficher une sonde", "Sur {outil}, câble/programme puis lis la sonde toutes les 2 s et affiche valeur + unité."),
            ("Moyenne glissante", "Échantillonne le capteur {n} fois et n'affiche que la moyenne glissante pour lisser les pics."),
            ("Seuil + alerte locale", "Déclenche {action} dès que la mesure sort de la plage {plage} ; ajoute un hystérésis."),
            ("Défaut capteur", "Traite la valeur aberrante (-273°C, 0 % figé) : détection, message, dernière valeur connue."),
            ("Calibration", "Étalonne {capteur} sur deux points connus et applique la correction à toute la chaîne."),
        ],
    },
    {
        "id": "action", "nom": "Commande & automation", "apps": "piloter un actionneur avec une logique métier claire.",
        "taches": [
            ("Asservissement simple", "{outil} : pilote {action} pour maintenir la mesure dans {plage}."),
            ("Horloge + scenarii", "Déclenche {action} selon l'heure (matin/soir/nuit) avec un programme MicroPython."),
            ("Anti-rebond", "{action} se déclenche en rafale à cause des rebonds : filtre matériel puis logiciel."),
            ("Séquence d'urgence", "Sur dépassement critique : séquence {n} actions dans le bon ordre avec journal."),
            ("Mode manuel/auto", "Bascule entre pilotage manuel (bouton) et automatique, sans code dupliqué."),
        ],
    },
    {
        "id": "mqtt", "nom": "MQTT & télémétrie", "apps": "publier/subscriber proprement et câbler un dashboard.",
        "taches": [
            ("Publier sur un topic", "Connecte le nœud à Mosquitto : publie {capteur} sur `labo/{lieu}/mesure` toutes les 5 s."),
            ("QoS et retenue", "Choisis QoS + message retenu pour qu'un dashboard redémarré affiche tout de suite la dernière valeur."),
            ("Subscription commande", "Le dashboard publie `labo/{lieu}/cmd` : le nœud exécute {action} selon le message."),
            ("Dash simple", "Tableau de bord (page web locale ou outil gratuit) : {n} capteurs, historique 24 h."),
            ("File d'attente offline", "Plus de réseau : met en file puis rejoue {n} mesures sans doublon au rebranchement."),
        ],
    },
    {
        "id": "energy", "nom": "Embarqué & contraintes", "apps": "penser batterie, sommeil et ressources limitées.",
        "taches": [
            ("Sommeil profond", "Réduis la conso : {action} toutes les {n} min, le reste du temps en deep sleep."),
            ("Stockage RAM limitée", "Stocke {n} mesures en mémoire limitée (buffer circulaire) sans explosion RAM."),
            ("Watchdog", "Ajoute un watchdog : si la boucle bloque > {n} s, reboot propre avec journal de la cause."),
            ("OTA léger", "Mise à jour du programme du nœud sans y toucher : mécanique de patch et rollback."),
            ("Batterie : estimer", "Estime l'autonomie à partir du cycle de mesure {n} et propose un réglage."),
        ],
    },
    {
        "id": "reseau-iot", "nom": "Intégration & protocole", "apps": "faire parler l'objet avec le monde : HTTP, JSON, horodatage.",
        "taches": [
            ("Télémétrie HTTP", "Publie la mesure en JSON vers l'API de labo : {capteur}, valeur, unité, horodatage ISO."),
            ("Réconciliation API", "Le serveur attend {n} nœuds : gère identifiants, tri et rejets avec code d'erreur."),
            ("Multi-capteurs", "Un nœud porte {n} capteurs : agrège en un message, schéma JSON documenté."),
            ("Pont MQTT <-> API", "Relais qui consomme les topics et alimente le dashboard Web via API locale."),
            ("Dossier de déploiement", "Documente le déploiement complet : topics, schémas, seuils, plan de test."),
        ],
    },
]

# Placeholders {…} résolus à l'exécution par le dictionnaire params.


def _paliers(n, rng):
    pool = []
    for p in range(1, 11):
        pool.extend([p] * (4 if p <= 4 else 3))
    while len(pool) < n:
        pool.extend(pool)
    rng.shuffle(pool)
    return pool[:n]


def generer(n: int, graine: int = 5):
    rng = random.Random(graine)
    rows = []
    paliers = _paliers(n, rng)
    combos = [(fam, tache) for fam in FAMILLES for tache in fam["taches"]]
    rng.shuffle(combos)

    for i in range(n):
        fam, tache = combos[i % len(combos)]
        palier = paliers[i]
        diff = difficulte(palier)
        lieu = rng.choice(LIEUX)
        params = {
            "capteur": rng.choice(CAPTEURS),
            "action": rng.choice(ACTIONNEURS).lower().strip(),
            "outil": rng.choice(BOITIERS),
            "lieu": lieu[0].replace(" ", "-"),
            "n": rng.randint(3, 60),
            "plage": f"{rng.randint(10, 40)}–{rng.randint(41, 90)}",
        }
        titre = tache[0].format(**params) if "{" in tache[0] else tache[0]
        demande = tache[1].format(**params)
        # Filet de sécurité si un formatage a laissé un blocage.
        if "{" in demande:
            demande = demande.split("{")[0].rstrip() + f" (config : {params['capteur']})"

        contexte = (
            f"À {lieu[0]}, le dispositif « {lieu[1]} » s'appuie sur {lieu[2]}. "
            f"Le montage est simulé sur {params['outil']} — aucun matériel requis. Scénario : {demande}"
        )
        probleme = (
            f"Le prototype {'bricole en Python sur PC' if palier <= 4 else 'tourne mais est fragile'} : "
            "il faut un nœud IoT qui tient dans la durée, avec contraintes réelles."
        )
        objectif = (
            f"Réaliser sur simulateur : {titre.lower()}. "
            "Livrable : câblage/schéma, code MicroPython (ou équivalent), sortie de test qui prouve le comportement."
        )
        environnement = f"{params['outil']}\nMicroPython\nTerminal\nMosquitto local pour les sujets MQTT"
        criteres_texte = criteres(
            f"Le comportement demandé est observé en simulation : {demande}",
            "Les valeurs publiées/affichées sont cohérentes avec le capteur choisi.",
            "Le montage est rejouable : schéma et code complet fournis.",
        )
        ce_que_tu_apprends = (
            f"{fam['nom']} : {fam['apps']} Tu maîtrises : {demande}"
        )
        themes = f"{fam['id']},iot"
        if palier >= 9:
            themes += ",projet"

        rows.append({
            "slug": slug_unique("iot", i, titre),
            "numero": 1,
            "titre": f"{fam['nom']} : {titre}"[:180],
            "accroche": f"{lieu[0].capitalize()} — {demande}"[:200],
            "duree": duree(palier),
            "langage": "python",
            "outils": f"{params['outil']}, Mosquitto (gratuit)"[:200],
            "palier": palier,
            "themes": themes,
            "type": "projet" if palier >= 9 else "exercice",
            "difficulte": diff,
            "contexte": contexte,
            "probleme": probleme,
            "objectif": objectif,
            "environnement": environnement,
            "contraintes": contraintes(palier),
            "amorce": f"# {titre}\n# Simulateur : {params['outil']}\n# Capteur : {params['capteur']}\n",
            "ce_que_tu_apprends": ce_que_tu_apprends,
            "criteres_texte": criteres_texte,
            "ordre": palier,
            "publiee": True,
        })
    return rows
