"""Générateur Réseaux : plans d'adressage, VLAN, routage, services, diagnostic.

Scénarios paramétrés (n réseaux, m hôtes, préfixes) sur Cisco Packet Tracer,
Wireshark et CLI — chaque énoncé reste vérifiable sur le papier ou en labo.
"""

import random

from .base import contraintes, criteres, difficulte, duree, slug_unique

ENTREPRISES = [
    "Lycée Technique Ampère", "CHU Sainte-Marie", "Mairie de Valmont", "Siège NordLog",
    "Groupe Scolaire Les Cèdres", "Usine Mécalux", "Cabinet Médical Pasteur", "Hôtel Belvue",
    "Port Maritime Océane", "Ferme Technopôle", "Collège Jean-Moulin", "Clinique Dentaire Horizon",
    "Entreprise BTP Charpente+", "Centre Commercial Rivage", "Association MediaCité", "Uside Chimie SafePro",
]

# (famille id, famille nom, préfixe slug, outils, langage, icone de tâche)
FAMILLES = [
    {
        "id": "adressage", "nom": "Plan d'adressage IP", "outils": "Cisco Packet Tracer",
        "langage": "texte",
        "taches": [
            ("Découper {prefix} en {n} sous-réseaux de taille égale",
             "Le réseau {prefix} doit être partagé en {n} sous-réseaux égaux pour {m} hôtes chacun au maximum."),
            ("Dimensionner un sous-réseau pour {m} hôtes",
             "Un service de {m} postes doit être isolé : choisis le préfixe le plus serré qui accommode {m} hôtes."),
            ("Découpage VLSM de {prefix} pour {n} services",
             "Le plan doit allouer {prefix} à {n} services de tailles différentes (VLSM), du plus gros au plus petit."),
            ("Vérifier une adresse et son masque",
             "Un poste configuré en {ip} /{p} ne communique pas : détermine réseau, diffusion et plage utilisables."),
            ("Résumer {n} réseaux en une route agrégée",
             "{n} réseaux /24 consécutifs à partir de {prefix} doivent être annoncés en un seul bloc (CIDR) au routeur central."),
        ],
    },
    {
        "id": "vlan", "nom": "VLAN & commutation", "outils": "Cisco Packet Tracer",
        "langage": "texte",
        "taches": [
            ("Créer {n} VLAN et câbler les accès",
             "Le switch central doit héberger {n} VLAN (data, voix, gestion, invités…) : crée-les et place les ports."),
            ("Configurer un trunk entre two switches",
             "Deux switchs doivent porter {n} VLAN en commun : mets en place le trunk et vérifie le passage."),
            ("Router entre VLAN (inter-VLAN routing)",
             "Les {n} VLAN doivent communiquer via le routeur (ou L3) : configure les passerelles."),
            ("Diagnostiquer un VLAN inaccessible",
             "Un poste du VLAN {vid} ne joint pas son serveur : traque l'erreur d'accès port/trunk."),
            ("Isoler le trafic de gestion",
             "Le management des switchs doit passer sur un VLAN dédié ({vid}) retiré des trunks utilisateurs."),
        ],
    },
    {
        "id": "routage", "nom": "Routage IP", "outils": "Cisco Packet Tracer",
        "langage": "texte",
        "taches": [
            ("Statique vs défaut : {n} routes",
             "Le routeur frontal doit joindre {n} réseaux internes : configure les routes statiques puis une route par défaut."),
            ("RIP entre {n} routeurs",
             "Topologie de {n} routeurs : fais converger RIP et vérifie les tables de routage."),
            ("OSPF multi-zones",
             "Le réseau est coupé en zones : configure OSPF, l'advertissage et vérifie le voisinage."),
            ("Policy-based : forcer un chemin",
             "Le trafic VoIP doit passer par le lien {lien}, le reste par l'autre : mets la politique en place."),
            ("VFR / partage de bande",
             "Deux liens WAN se partagent le trafic : configure un routage et QoS simple qui tient la charge."),
        ],
    },
    {
        "id": "services", "nom": "DHCP / DNS", "outils": "Cisco Packet Tracer, Serveurs de labo",
        "langage": "texte",
        "taches": [
            ("Pool DHCP pour {n} réseaux",
             "Configure un pool DHCP par VLAN ({n} pools) avec réservations pour les imprimantes et passerelles."),
            ("Exclusions et réservations DHCP",
             "Le pool {prefix} doit exclure les {r} premières adresses et réserver {m} postes fixes."),
            ("Zone DNS interne",
             "Le nom {domaine} doit résoudre vers {n} serveurs internes : monte la zone et teste."),
            ("DHCP relais inter-VLAN",
             "Le serveur DHCP n'est que dans un VLAN : configure le relais pour les {n} autres réseaux."),
            ("Panne de service : DHCP ou DNS",
             "Les postes obtiennent une IP mais ne résolvent rien : isole la panne couche par couche."),
        ],
    },
    {
        "id": "nat-acl", "nom": "NAT & ACL", "outils": "Cisco Packet Tracer",
        "langage": "texte",
        "taches": [
            ("NAT PAT pour {m} postes",
             "Seule une IP publique est disponible : configure le NAT PAT pour {m} postes du LAN {prefix}."),
            ("NAT statique vers un serveur",
             "Le serveur web {ip} doit être joignable depuis l'extérieur : mets le NAT statique en place."),
            ("ACL : bloquer {n} services",
             "La politique interdit {n} flux précis (telnet, SMB…) : écris l'ACL et applique-la dans le bon sens."),
            ("ACL par adresse source",
             "Seuls les réseaux {prefix}.0 doivent joindre le serveur finances : exprime la règle exacte."),
            ("Audit d'une ACL qui casse tout",
             "Après une modification, plus personne n'accède au serveur : relis l'ACL ligne par ligne."),
        ],
    },
    {
        "id": "wifi", "nom": "Réseaux sans fil", "outils": "Cisco Packet Tracer, routeur Wi-Fi de labo",
        "langage": "texte",
        "taches": [
            ("Trois SSID, trois VLANs",
             "Le site doit diffuser un réseau employés, invités et cours {n} SSID isolés : planifie-les."),
            ("WPA2/WPA3 : choix et configuration",
             "Le point d'accès doit être sécurisé au niveau maximal compatible : configure et justifie."),
            ("Couverture : placement des bornes",
             "Le plan du bâtiment montre {n} zones mortes : place les bornes et les canaux pour les couvrir."),
            ("Roaming entre AP",
             "La mobilité des utilisateurs entre {n} bornes provoque des coupures : corrige la configuration."),
            ("Diagnostic d'un Wi-Fi saturé",
             "Le débit s'effondre en fin de journée : analyse canaux, interférences et taille de cellule."),
        ],
    },
    {
        "id": "diagnostic", "nom": "Diagnostic & dépannage", "outils": "Terminal / invite de commandes, Ping, Traceroute",
        "langage": "texte",
        "taches": [
            ("Panne couche par couche",
             "Un poste ne sort pas du réseau : applique la méthode OSI (物理 → applicative) et trouve la cause."),
            ("Lecture d'un tracé de route",
             "Le traceroute vers {domaine} échoue au saut {s} : interprète et propose la correction."),
            ("Comparaison avant/après",
             "Une modification de switch a cassé {m} postes : compare les configs et identifie le changement fautif."),
            ("Câblage et LED",
             "Le lien ne monte pas : détermine, symptômes à l'appui, si le défaut est physique ou logique."),
            ("IP en conflit",
             "Deux postes revendiquent {ip} : explique le mécanisme et empêche le renouvellement du conflit."),
        ],
    },
    {
        "id": "capture", "nom": "Analyse de trames (Wireshark)", "outils": "Wireshark",
        "langage": "python",
        "taches": [
            ("Filtrer et compter",
             "Sur la capture {pcap}, compte les trames par protocole avec un filtre d'affichage."),
            ("Suivre un flux TCP",
             "Retrouve la conversation complète entre {ip} et le serveur : décris les étapes et les statuts."),
            ("Repérer une diffusion anormale",
             "La capture montre un pic de {n} paquets/seconde : identifie la source et la nature du trafic."),
            ("Analyse ARP",
             "Des réponses ARP arrivent avant les requêtes : explique le phénomène et repère l'attaquant."),
            ("Script d'analyse",
             "Écris un script (Python ou traitement texte) qui résume {pcap} : top protocoles, adresses, pics de trafic."),
        ],
    },
]

EXTRA = [
    "La direction réseau veut un livrable clair : schéma + tables d'adressage commentées.",
    "La topologie est fournie en fichier .pkt ; on ne change pas le câblage existant.",
    "Toute config doit être rejouable : pense sauvegarde startup-config.",
    "Le stage réseau dure deux heures : restons dans le périmètre de l'énoncé.",
    "Le plan actuel est approximatif : la refactorisation doit être justifiable.",
]

PALETS = ["10", "20", "30", "50", "80", "120", "200", "250"]
PREFIXES = ["192.168.10.0/24", "10.20.0.0/16", "172.16.4.0/22", "192.168.50.0/24",
            "10.8.0.0/21", "192.168.0.0/16", "10.10.0.0/23", "172.16.0.0/20"]
DOMAINS = ["intranet.local", "labo.local", "reseau.local", "atelier.local"]
PCAPS = ["capture-matinee.pcapng", "reseau-sante.pcapng", "pcap-usine.pcapng", "flux-douteux.pcapng"]
LIENS = ["Lien 1 (fib)", "Lien 2 (cuivre)", "lien principal", "lien de secours"]


def _paliers(n, rng):
    pool = []
    for p in range(1, 11):
        pool.extend([p] * (4 if p <= 4 else 3))
    while len(pool) < n:
        pool.extend(pool)
    rng.shuffle(pool)
    return pool[:n]


def generer(n: int, graine: int = 7):
    rng = random.Random(graine)
    rows = []
    paliers = _paliers(n, rng)
    combos = [(fam, tache) for fam in FAMILLES for tache in fam["taches"]]
    rng.shuffle(combos)

    for i in range(n):
        fam, tache = combos[i % len(combos)]
        palier = paliers[i]
        diff = difficulte(palier)
        params = {
            "n": rng.randint(2, 9),
            "m": rng.choice(PALETS),
            "prefix": rng.choice(PREFIXES),
            "ip": f"192.168.{rng.randint(0, 250)}.{rng.randint(2, 250)}",
            "p": rng.choice([23, 24, 25, 26, 27, 28]),
            "vid": rng.randint(10, 400),
            "r": rng.randint(5, 20),
            "domaine": rng.choice(DOMAINS),
            "pcap": rng.choice(PCAPS),
            "lien": rng.choice(LIENS),
            "s": rng.randint(2, 11),
        }
        entreprise = rng.choice(ENTREPRISES)
        consigne = rng.choice(EXTRA)
        titre = tache[0].format(**params)
        if palier >= 7:
            titre = f"{titre} — niveau ops"
        demande = tache[1].format(**params)

        contexte = f"{entreprise} exploite un réseau interne qui doit évoluer. {consigne} {demande}"
        probleme = (
            f"Le plan réseau actuel est {'documenté en grande partie à la main' if palier <= 4 else 'hérité, avec des incohérences entre équipements'} : "
            f"les pannes et les erreurs de configuration coûtent du temps à toute l'équipe."
        )
        objectif = (
            f"Dans {fam['outils'].split(',')[0].strip()}, réaliser la tâche : {titre.lower()}. "
            f"Produire la configuration (ou l'analyse) complète, le schéma à jour et une vérification qui prouve le résultat."
        )
        environnement = (
            f"Outil principal : {fam['outils']}\nPoste : Windows/Linux\n"
            f"Adresse de référence : {params['prefix']} — domaine de labo : {params['domaine']}"
        )
        criteres_texte = criteres(
            f"La configuration/analyse répond précisément à : {demande}",
            "Les adresses, masques et passerelles annoncés sont cohérents entre le schéma et les équipements.",
            "Une commande ou un test de vérification est fourni et son résultat est interprété.",
        )
        ce_que_tu_apprends = (
            f"{fam['nom']} : savoir concevoir, configurer et dépanner un segment réseau professionnel. "
            f"Tu maîtrises : {demande}"
        )
        themes = f"{fam['id']},reseau"
        if palier >= 9:
            themes += ",projet"

        rows.append({
            "slug": slug_unique("rs", i, titre),
            "numero": 1,
            "titre": f"{fam['nom']} : {titre}"[:180],
            "accroche": f"{entreprise} : {demande}"[:200],
            "duree": duree(palier),
            "langage": fam["langage"],
            "outils": fam["outils"][:200],
            "palier": palier,
            "themes": themes,
            "type": "projet" if palier >= 9 else "exercice",
            "difficulte": diff,
            "contexte": contexte,
            "probleme": probleme,
            "objectif": objectif,
            "environnement": environnement,
            "contraintes": contraintes(palier),
            "amorce": f"# {titre}\n# Outils : {fam['outils']}\n# Topologie de labo — consigne : {demande}\n",
            "ce_que_tu_apprends": ce_que_tu_apprends,
            "criteres_texte": criteres_texte,
            "ordre": palier,
            "publiee": True,
        })
    return rows
