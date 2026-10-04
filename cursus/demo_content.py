"""Contenu de démonstration réaliste, entièrement en français.

Structure : domaines -> compétences -> notions + missions.
Chaque mission suit la structure imposée : contexte, problème, objectif,
environnement, étapes, contraintes, indices, critères de validation.
"""

CONTENU = [
    # =====================================================================
    {
        "domaine": {
            "titre": "Python", "icone": "code-2", "couleur": "bleu", "ordre": 1,
            "sous_titre": "Automatiser les tâches réelles d'une entreprise",
            "description": "Scripter pour résoudre des problèmes concrets : fichiers, logs, API, administration système.",
        },
        "competences": [
            {
                "titre": "Python de base", "niveau": "debutant", "ordre": 1,
                "description": "Les briques essentielles pour écrire un script utile.",
                "notions": [
                    {"titre": "Variables & types", "resume": "str, int, bool, list, dict. Le dict est la base de la plupart des automatisations."},
                    {"titre": "Conditions & boucles", "resume": "if/for/while servent à traiter un lot d'éléments sans tout écrire à la main."},
                    {"titre": "Fonctions", "resume": "Une fonction = une opération réutilisable et testable. Toujours la découper proprement."},
                ],
                "missions": [
                    {
                        "numero": 1, "titre": "Vérifier la conformité des mots de passe internes",
                        "type": "exercice", "difficulte": "debutant",
                        "contexte": "Une PME doit appliquer une politique de sécurité : les utilisateurs ne peuvent pas choisir n'importe quel mot de passe.",
                        "probleme": "Aucun contrôle n'existe et l'administrateur valide à la main, lentement et de façon incohérente.",
                        "objectif": "Écrire un script qui teste une liste de mots de passe et renvoie lesquels respectent la politique.",
                        "environnement": "Python 3\nVS Code\nTerminal",
                        "contraintes": "Pas de dépendance externe. Fonction pure, testable. Respect de la longueur minimale et des classes de caractères.",
                        "etapes": [
                            "Récupérer une liste de mots de passe à tester",
                            "Écrire une fonction evaluer(mdp) qui renvoie True/False",
                            "Vérifier la longueur minimale (8 caractères)",
                            "Vérifier majuscule, minuscule, chiffre, caractère spécial",
                            "Afficher le rapport pour la liste complète",
                        ],
                        "indices": [
                            "Utilisez any(c.isdigit() for c in mdp) pour tester la présence d'un chiffre.",
                            "Découpez la vérification en petites fonctions : un test = une fonction.",
                            "Un mot de passe invalide ne doit pas faire planter le script : renvoyez simplement False.",
                        ],
                        "criteres": [
                            "La fonction renvoie booléen sans lever d'exception",
                            "Un mot de passe trop court est bien rejeté",
                            "Le rapport final liste les acceptés et les rejetés",
                        ],
                    },
                ],
            },
            {
                "titre": "Fichiers & automatisation", "niveau": "intermediaire", "ordre": 2,
                "description": "Lire, écrire et transformer des données pour supprimer le travail manuel répétitif.",
                "notions": [
                    {"titre": "Lecture/écriture de fichiers", "resume": "open() avec gestion by-name, CSV et JSON couvrent 90 % des besoins d'automatisation."},
                    {"titre": "Exceptions", "resume": "try/except évite qu'un fichier manquant ne fasse tomber toute la tâche planifiée."},
                    {"titre": "Structures de données", "resume": "dict et list modélisent proprement des utilisateurs, des tâches ou des enregistrements."},
                ],
                "missions": [
                    {
                        "numero": 2, "titre": "Automatiser la gestion des utilisateurs d'une entreprise",
                        "type": "projet", "difficulte": "intermediaire",
                        "contexte": "Une PME possède plusieurs serveurs et doit régulièrement créer, modifier et désactiver des comptes utilisateurs.",
                        "probleme": "L'administrateur réalise toutes ces opérations manuellement et perd beaucoup de temps, avec un fort risque d'erreur.",
                        "objectif": "Créer un script Python qui lit un fichier d'entrée et applique les opérations de gestion des comptes.",
                        "environnement": "Python 3\nVS Code\nWindows / Linux\nTerminal\nFichier CSV",
                        "contraintes": "Le script doit être idempotent, journaliser chaque action, et ne jamais écraser un fichier existant sans backup. Gestion des erreurs obligatoire.",
                        "etapes": [
                            "Décrire le format d'entrée (CSV : action,username,role,email)",
                            "Lire le fichier et créer une entrée par utilisateur (dict)",
                            "Implémenter create / update / disable",
                            "Écrire l'état final dans un fichier JSON de référence",
                            "Ajouter la gestion des exceptions (fichier manquant, ligne invalide)",
                            "Journaliser chaque opération horodatée",
                        ],
                        "indices": [
                            "Modélisez un utilisateur par un dict : {'username':..., 'role':..., 'active':True}.",
                            "Séparez la logique métier (fonctions) de la lecture du fichier : c'est plus testable.",
                            "Utilisez le module logging au lieu de print() pour la journalisation professionnelle.",
                            "Sauvegardez l'ancien JSON avant d'écrire le nouveau.",
                        ],
                        "criteres": [
                            "Un utilisateur inexistant est créé, un existant est mis à jour",
                            "La désactivation ne supprime pas la ligne mais passe 'active' à False",
                            "Une ligne malformée est ignorée et journalisée sans interrompre le script",
                            "Un fichier de log horodaté est produit",
                        ],
                        "mobilise": ["Python de base", "Fichiers & automatisation", "Sécurité des accès", "Linux & bases sécurité"],
                    },
                    {
                        "numero": 3, "titre": "Analyser automatiquement les logs d'un serveur",
                        "type": "exercice", "difficulte": "intermediaire",
                        "contexte": "Un serveur applicatif produit un fichier de log quotidien de plusieurs dizaines de milliers de lignes.",
                        "probleme": "Aucun outil ne résume l'activité : impossible de voir rapidement les erreurs récurrentes.",
                        "objectif": "Produire un rapport synthétique : nombre d'erreurs par code, IP les plus actives, créneaux horaires critiques.",
                        "environnement": "Python 3\nTerminal\nFichier.log",
                        "contraintes": "Le script doit traiter le fichier sans le charger entièrement en mémoire (lecture ligne à ligne).",
                        "etapes": [
                            "Définir le format de log à parser",
                            "Compter les erreurs par statut",
                            "Extraire et agréger les adresses IP",
                            "Identifier le créneau horatoire le plus chargé",
                            "Générer un petit rapport texte",
                        ],
                        "indices": [
                            "Utilisez collections.Counter pour agréger rapidement.",
                            "Re.compile() une seule fois, hors de la boucle.",
                            "Lisez le fichier avec 'for line in f:' pour rester économe en mémoire.",
                        ],
                        "criteres": [
                            "Le rapport affiche le top 5 des IP",
                            "Le nombre total d'erreurs est correct",
                            "Le script tourne sur un fichier de 100 000 lignes sans exploser en mémoire",
                        ],
                        "mobilise": ["Fichiers & automatisation", "Analyse & détection d'incidents"],
                    },
                ],
            },
            {
                "titre": "API & réseau en Python", "niveau": "avance", "ordre": 3,
                "description": "Dialoguer avec des services et surveiller des systèmes à distance.",
                "notions": [
                    {"titre": "Requêtes HTTP", "resume": "requests encapsule verbes, en-têtes et statut — la base de toute intégration."},
                    {"titre": "JSON & sérialisation", "resume": "Les API échangent du JSON ; dict <--> json est quotidien."},
                    {"titre": "Gestion des erreurs réseau", "resume": "Timeouts et retry : une API tombe toujours au mauvais moment."},
                ],
                "missions": [
                    {
                        "numero": 4, "titre": "Interroger l'API de supervision du datacenter",
                        "type": "projet", "difficulte": "avance",
                        "contexte": "L'équipe exploitation veut un tableau de bord texte quotidien produit à partir de l'API de supervision.",
                        "probleme": "Les données existent mais sont inaccessibles sans requêtes API et traitement automatique.",
                        "objectif": "Écrire un client Python qui interroge l'API, gère les erreurs et publie un rapport d'état.",
                        "environnement": "Python 3\nAPI REST (httpbin/localhost)\nGit\nTerminal",
                        "contraintes": "Authentification par token, gestion des codes 4xx/5xx, timeout explicite, aucune lueur de secret en dur.",
                        "etapes": [
                            "Lire le token depuis une variable d'environnement",
                            "Écrire une fonction get(path) avec en-têtes d'auth",
                            "Gérer timeout et codes d'erreur",
                            "Parser la réponse JSON en objets utiles",
                            "Formater un rapport d'état lisible",
                        ],
                        "indices": [
                            "os.environ['SUPERVISOR_TOKEN'] — jamais le token en clair dans le code.",
                            "requests.get(url, timeout=5) sinon le script peut se figer.",
                            "Répondez différemment à une 4xx (erreur de requête) et une 5xx (panne serveur).",
                        ],
                        "criteres": [
                            "Le script ne crash pas sur une 500 : il journalise et continue",
                            "Le token n'apparaît jamais dans le code ni les logs",
                            "Un rapport d'état clair est produit",
                        ],
                        "mobilise": ["API & réseau en Python", "Pentest & rapport"],
                    },
                ],
            },
        ],
    },

    # =====================================================================
    {
        "domaine": {
            "titre": "Réseaux informatiques", "icone": "network", "couleur": "violet", "ordre": 2,
            "sous_titre": "Concevoir, configurer et dépanner des réseaux d'entreprise",
            "description": "Du LAN de la nouvelle agence au routage multi-sites, en passant par VLAN et DHCP.",
        },
        "competences": [
            {
                "titre": "Fondamentaux IP & LAN", "niveau": "debutant", "ordre": 1,
                "description": "Adressage IPv4, masque, passerelle : comprendre qui parle à qui.",
                "notions": [
                    {"titre": "IPv4 & masque", "resume": "Adresse + masque définissent le réseau et les hôtes. /24 = 254 postes utilisables."},
                    {"titre": "Passerelle", "resume": "La porte de sortie du LAN vers les autres réseaux."},
                    {"titre": "ICMP & ping", "resume": "Premier outil de diagnostic de connectivité."},
                ],
                "missions": [
                    {
                        "numero": 1, "titre": "Mettre en place le réseau local d'une nouvelle agence",
                        "type": "projet", "difficulte": "debutant",
                        "contexte": "Une entreprise vient d'installer plusieurs ordinateurs dans une nouvelle agence et doit mettre en place son réseau local.",
                        "probleme": "Les machines doivent pouvoir communiquer entre elles et sortir sur Internet, de façon ordonnée et documentée.",
                        "objectif": "Conceiller et configurer l'adressage IP du LAN et vérifier la connectivité.",
                        "environnement": "Cisco Packet Tracer\nSwitch\nPC / serveurs\nTerminal (ping, ipconfig)",
                        "contraintes": "Plage d'adresses cohérente, passerelle unique, documenter le plan d'adressage.",
                        "etapes": [
                            "Choisir un réseau (ex. 192.168.10.0/24)",
                            "Attribuer IP/masque/passerelle à chaque poste",
                            "Configurer la passerelle du routeur",
                            "Vérifier la connectivité avec ping",
                            "Rédiger le plan d'adressage",
                        ],
                        "indices": [
                            "Dans un /24, le routeur prend souvent la 1re ou la dernière adresse utilisable.",
                            "Deux postes sur le même réseau mais qui ne se 'pingent' pas = masque ou IP incohérente.",
                            "Un ping vers la passerelle teste le LAN ; un ping vers 8.8.8.8 teste la sortie.",
                        ],
                        "criteres": [
                            "Tous les postes ont une IP unique et un masque identique",
                            "Le ping entre postes fonctionne",
                            "Le ping vers la passerelle fonctionne",
                            "Le plan d'adressage est documenté",
                        ],
                        "mobilise": ["Fondamentaux IP & LAN"],
                    },
                ],
            },
            {
                "titre": "Services réseau (DHCP / DNS)", "niveau": "intermediaire", "ordre": 2,
                "description": "Industrialiser l'adressage et la résolution de noms.",
                "notions": [
                    {"titre": "DHCP & pool", "resume": "Attribution automatique des adresses ; exclure les adresses fixes du pool."},
                    {"titre": "DNS", "resume": "Nom <-> IP ; indispensable pour accéder aux services autrement qu'à coups d'IP."},
                ],
                "missions": [
                    {
                        "numero": 2, "titre": "Automatiser l'attribution des adresses IP",
                        "type": "projet", "difficulte": "intermediaire",
                        "contexte": "L'agence s'agrandit : attribuer une IP fixe à chaque poste devient ingérable.",
                        "probleme": "Le parc grandit, les conflits d'adresses apparaissent, la config manuelle ne scale plus.",
                        "objectif": "Mettre en place un serveur DHCP avec un pool cohérent et des réservations pour les équipements fixes.",
                        "environnement": "Cisco Packet Tracer\nServeur DHCP\nWindows client\nTerminal",
                        "contraintes": "Exclure les adresses des serveurs imprimantes du pool, réserver les IP critiques, fournir DNS et passerelle.",
                        "etapes": [
                            "Définir le pool DHCP (plage excluant les IP fixes)",
                            "Configurer passerelle, DNS et masque distribués",
                            "Créer des réservations pour les serveurs/imprimantes",
                            "Tester l'obtention d'une IP depuis un client",
                            "Vérifier l'absence de conflit d'adresses",
                        ],
                        "indices": [
                            "Une réservation relie une IP fixe à une adresse MAC.",
                            "Oublier d'exclure l'IP de la passerelle du pool provoque des conflits.",
                            "Sur un client Windows : ipconfig /release puis /renew.",
                        ],
                        "criteres": [
                            "Un client obtient automatiquement une IP valide",
                            "Les équipements fixes gardent toujours la même adresse",
                            "Aucun conflit d'IP détecté",
                        ],
                        "mobilise": ["Services réseau (DHCP / DNS)", "Fondamentaux IP & LAN"],
                    },
                ],
            },
            {
                "titre": "Segmentation & routage", "niveau": "avance", "ordre": 3,
                "description": "Séparer les flux et relier les réseaux qui doivent communiquer.",
                "notions": [
                    {"titre": "VLAN & trunk", "resume": "Segmenter un switch en plusieurs réseaux logiques ; un lien trunk transporte plusieurs VLAN."},
                    {"titre": "Routage statique / dynamique", "resume": "Faire communiquer des réseaux distincts via des routes."},
                ],
                "missions": [
                    {
                        "numero": 3, "titre": "Séparer les services sensibles avec des VLAN",
                        "type": "projet", "difficulte": "avance",
                        "contexte": "Une entreprise possède plusieurs services (comptabilité, production, invités) qui doivent être isolés sur le même réseau physique.",
                        "probleme": "Tout le monde est sur le même LAN : un poste compromis atteint tous les services.",
                        "objectif": "Mettre en place une segmentation par VLAN et contrôler la communication entre zones.",
                        "environnement": "Cisco Packet Tracer\nSwitch manageable\nRouteur (inter-VLAN)\nTerminal",
                        "contraintes": "Un VLAN par service, lien trunk entre switch et routeur, le VLAN invités ne doit pas joindre la production.",
                        "etapes": [
                            "Définir un VLAN par service avec son sous-réseau",
                            "Affecter les ports d'accès aux bons VLAN",
                            "Configurer le lien trunk",
                            "Mettre en place le routage inter-VLAN",
                            "Tester que la segmentation est respectée",
                        ],
                        "indices": [
                            "Un port d'accès porte un seul VLAN ; un port trunk en porte plusieurs.",
                            "Le routage inter-VLAN 'single-arm' utilise des sous-interfaces.",
                            "Testez les deux sens : production->compta OK, invités->production refusé.",
                        ],
                        "criteres": [
                            "Chaque service est dans son propre sous-réseau",
                            "Le lien trunk transporte plusieurs VLAN",
                            "Le VLAN invités ne peut pas atteindre la production",
                        ],
                        "mobilise": ["Segmentation & routage", "Sécurité réseau"],
                    },
                    {
                        "numero": 4, "titre": "Relier les réseaux de deux sites",
                        "type": "projet", "difficulte": "avance",
                        "contexte": "L'entreprise a ouvert un second site ; les deux réseaux doivent se joindre.",
                        "probleme": "Aucun chemin entre les réseaux : les sites sont isolés.",
                        "objectif": "Mettre en place le routage entre les deux sites.",
                        "environnement": "Cisco Packet Tracer\n2 routeurs\nTerminal",
                        "contraintes": "Route statique ou dynamique, vérification de bout en bout.",
                        "etapes": [
                            "Recenser les réseaux de chaque site",
                            "Configurer les interfaces routeur",
                            "Ajouter les routes (statiques ou OSPF)",
                            "Vérifier le chemin avec traceroute",
                            "Tester la connectivité d'un site à l'autre",
                        ],
                        "indices": [
                            "Une route statique pointe un réseau distant vers l'IP voisine.",
                            "traceroute révèle où le paquet se perd.",
                        ],
                        "criteres": [
                            "Un poste du site A atteint un poste du site B",
                            "traceroute suit le bon chemin",
                            "La config est documentée",
                        ],
                        "mobilise": ["Segmentation & routage", "Fondamentaux IP & LAN"],
                    },
                ],
            },
        ],
    },

    # =====================================================================
    {
        "domaine": {
            "titre": "Cybersécurité", "icone": "shield", "couleur": "rouge", "ordre": 3,
            "sous_titre": "Défendre, détecter et tester — dans des laboratoires autorisés",
            "description": "Sécurité Linux, analyse de logs/trafic, web, et pentest professionnel en environnement isolé.",
        },
        "competences": [
            {
                "titre": "Linux & bases sécurité", "niveau": "debutant", "ordre": 1,
                "description": "La plateforme de la plupart des systèmes et des outils de sécurité.",
                "notions": [
                    {"titre": "Commandes essentielles", "resume": "ls, cd, grep, cat, ps : l'atelier quotidien."},
                    {"titre": "Permissions", "resume": "lecture/écriture/exécution par propriétaire, groupe, autres. Le moindre privilège commence ici."},
                ],
                "missions": [
                    {
                        "numero": 1, "titre": "Durcir l'accès SSH d'un serveur",
                        "type": "exercice", "difficulte": "debutant",
                        "contexte": "Un serveur Linux exposé accepte les connexions SSH en root par mot de passe.",
                        "probleme": "Cette configuration est la première cible des attaques par force brute.",
                        "objectif": "Appliquer un durcissement SSH standard en environnement maîtrisé.",
                        "environnement": "Linux\nTerminal\n/etc/ssh/sshd_config",
                        "contraintes": "Ne pas se verrouiller hors du serveur : garder une session de secours et valider la config avant de redémarrer.",
                        "etapes": [
                            "Créer un utilisateur admin non-root",
                            "Interdire la connexion root par SSH",
                            "Privilégier l'authentification par clé",
                            "Valider la syntaxe puis redémarrer sshd",
                            "Tester la connexion depuis un poste client",
                        ],
                        "indices": [
                            "PermitRootLogin no et PasswordAuthentication no dans sshd_config.",
                            "sshd -t valide la configuration sans couper la session en cours.",
                        ],
                        "criteres": [
                            "La connexion root en SSH est refusée",
                            "La connexion par clé fonctionne",
                            "Le serveur reste accessible via l'utilisateur admin",
                        ],
                        "mobilise": ["Linux & bases sécurité", "Sécurité des accès"],
                    },
                ],
            },
            {
                "titre": "Sécurité des accès", "niveau": "intermediaire", "ordre": 2,
                "description": "Authentification, contrôle d'accès, sessions et mots de passe.",
                "notions": [
                    {"titre": "Authentification", "resume": "Qui es-tu ? Mots de passe forts, clés, MFA."},
                    {"titre": "Contrôle d'accès", "resume": "As-tu le droit ? Le moindre privilège limite l'impact d'une compromission."},
                ],
                "missions": [],
            },
            {
                "titre": "Analyse & détection d'incidents", "niveau": "intermediaire", "ordre": 3,
                "description": "Comprendre ce qui s'est passé à partir des traces disponibles.",
                "notions": [
                    {"titre": "Analyse de logs", "resume": "Les logs racontent l'histoire : qui, quoi, quand, d'où."},
                    {"titre": "Analyse de trafic", "resume": "Wireshark capture les échanges réels, y compris ce qu'on voudrait cacher."},
                ],
                "missions": [
                    {
                        "numero": 2, "titre": "Analyste sécurité : activité inhabituelle sur un serveur interne",
                        "type": "laboratoire", "difficulte": "intermediaire",
                        "contexte": "Vous êtes analyste sécurité dans une PME. L'équipe informatique constate une activité inhabituelle sur un serveur interne.",
                        "probleme": "Plusieurs connexions semblent provenir d'un poste interne à des heures anormales.",
                        "objectif": "Analyser les traces disponibles et déterminer ce qui s'est passé, puis proposer des mesures correctives.",
                        "environnement": "Linux\nWireshark\nFichiers de logs\nEnvironnement de laboratoire",
                        "contraintes": "Raisonner à partir des seules traces fournies. Distinguer un comportement légitime d'un comportement suspect avant de conclure.",
                        "etapes": [
                            "Analyser les logs et repérer les heures anormales",
                            "Identifier les IP impliquées",
                            "Rechercher les connexions suspectes",
                            "Analyser le trafic avec Wireshark",
                            "Identifier le service concerné",
                            "Formuler une hypothèse d'incident",
                            "Proposer des mesures correctives",
                        ],
                        "indices": [
                            "Grouper les logs par IP source fait ressortir l'anomalie.",
                            "Dans Wireshark, le filtre 'ip.addr == X' isole un hôte.",
                            "Un transfert sortant volumineux à 3h du matin est un signal faible à croiser.",
                        ],
                        "criteres": [
                            "L'IP d'origine des connexions suspectes est identifiée",
                            "Le service concerné est déterminé",
                            "Une hypothèse d'incident étayée par les traces est formulée",
                            "Des mesures correctives concrètes sont proposées",
                        ],
                        "mobilise": ["Analyse & détection d'incidents", "Linux & bases sécurité", "Sécurité réseau"],
                    },
                ],
            },
            {
                "titre": "Reconnaissance en laboratoire", "niveau": "intermediaire", "ordre": 4,
                "description": "Cartographier une cible autorisée, comme le fait un pro avant un pentest.",
                "notions": [
                    {"titre": "Nmap", "resume": "Découverte d'hôtes, ports ouverts et services. Le réflexe de tout auditeur."},
                    {"titre": "Empreinte de services", "resume": "Versions et services exposés = surface d'attaque."},
                ],
                "missions": [
                    {
                        "numero": 3, "titre": "Scanner un hôte de laboratoire autorisé",
                        "type": "laboratoire", "difficulte": "intermediaire",
                        "contexte": "Un auditeur doit évaluer l'exposition d'une machine de laboratoire volontairement vulnérable, explicitement autorisée.",
                        "probleme": "Sans inventaire des ports et services, impossible de prioriser les risques.",
                        "objectif": "Identifier les ports ouverts, les services et leurs versions, puis documenter la surface d'attaque.",
                        "environnement": "Linux\nNmap\nMachine de laboratoire\nLABORATOIRE AUTORISÉ — ENVIRONNEMENT DE FORMATION",
                        "contraintes": "Scanner UNIQUEMENT la machine de laboratoire assignée. Toute cible réelle est interdite sans autorisation écrite.",
                        "etapes": [
                            "Vérifier le périmètre autorisé (scope)",
                            "Découvrir l'hôte (ping / -sn)",
                            "Scanner les ports (service + version)",
                            "Documenter chaque service exposé",
                            "Classer les risques par criticité",
                        ],
                        "indices": [
                            "nmap -sV cible <IP_LABO> pour services et versions.",
                            "Toujours confirmer l'autorisation avant tout scan.",
                            "Un port ouvert n'est pas forcément vulnérable : croisez avec les versions.",
                        ],
                        "criteres": [
                            "Le périmètre autorisé est explicitement rappelé",
                            "La liste des ports ouverts et services est produite",
                            "Chaque service est associé à un niveau de risque",
                        ],
                        "mobilise": ["Reconnaissance en laboratoire", "Sécurité réseau"],
                    },
                ],
            },
            {
                "titre": "Sécurité applicative web", "niveau": "avance", "ordre": 5,
                "description": "Comprendre les vulnérabilités web pour les détecter et les corriger.",
                "notions": [
                    {"titre": "Injection SQL", "resume": "Entrées non filtrées exécutées comme du code. Requêtes paramétrées = remède."},
                    {"titre": "XSS", "resume": "Script injecté exécuté dans le navigateur d'une victime. Échappement de sortie."},
                    {"titre": "CSRF", "resume": "Action forcée via une session valide. Jetons anti-CSRF."},
                ],
                "missions": [
                    {
                        "numero": 4, "titre": "Identifier et corriger une injection SQL (laboratoire vulnérable)",
                        "type": "laboratoire", "difficulte": "avance",
                        "contexte": "Une application web de laboratoire, volontairement vulnérable et isolée, gère des comptes clients via un formulaire de recherche.",
                        "probleme": "Le champ de recherche construit une requête SQL par concaténation.",
                        "objectif": "Démontrer la faille en environnement autorisé, puis proposer et valider la correction.",
                        "environnement": "Application web de laboratoire\nBrowser\nLABORATOIRE AUTORISÉ — ENVIRONNEMENT DE FORMATION",
                        "contraintes": "Travailler uniquement sur l'application de laboratoire. Produire une preuve de concept et un correctif, pas d'exfiltration de données réelles.",
                        "etapes": [
                            "Repérer le point d'entrée (champ de recherche)",
                            "Confirmer le comportement d'injection (PoC contrôlée)",
                            "Expliquer l'impact potentiel",
                            "Proposer la requête paramétrée correspondante",
                            "Vérifier que la correction bloque l'injection",
                        ],
                        "indices": [
                            "Un caractère ' qui casse la requête est un signal fort.",
                            "Le remède n'est pas de filtrer les caractères mais de séparer code et données (requêtes paramétrées).",
                        ],
                        "criteres": [
                            "La preuve de concept est réalisée sur la cible de laboratoire uniquement",
                            "L'impact est expliqué en termes métier",
                            "Un correctif par requête paramétrée est proposé",
                        ],
                        "mobilise": ["Sécurité applicative web", "Analyse & détection d'incidents"],
                    },
                ],
            },
            {
                "titre": "Pentest & rapport", "niveau": "expert", "ordre": 6,
                "description": "La méthode professionnelle complète : du scope au rapport de remédiation.",
                "notions": [
                    {"titre": "Méthode pentest", "resume": "Scope/autorisation → reco → énumération → vulnérabilités → validation → impact → remédiation → rapport."},
                    {"titre": "Rapport", "resume": "Un bon rapport permet de corriger : criticité, preuve, impact, remédiation."},
                ],
                "missions": [
                    {
                        "numero": 5, "titre": "Pentest complet d'un serveur de laboratoire",
                        "type": "pentest", "difficulte": "expert",
                        "contexte": "Vous menez une mission de pentest sur un serveur de laboratoire volontairement vulnérable, dans un environnement de formation explicitement autorisé.",
                        "probleme": "L'organisation doit connaître son exposition réelle et prioriser les corrections.",
                        "objectif": "Conduire la démarche professionnelle complète et produire un rapport exploitable.",
                        "environnement": "Linux\nNmap\nWireshark\nMachine de laboratoire\nLABORATOIRE AUTORISÉ — ENVIRONNEMENT DE FORMATION",
                        "contraintes": "Cadre strict : périmètre délimité et autorisation écrite préalable. Aucune cible réelle. Toute action offensive reste dans le laboratoire.",
                        "etapes": [
                            "Définir le scope et confirmer l'autorisation",
                            "Réaliser la reconnaissance et l'énumération",
                            "Identifier les vulnérabilités",
                            "Valider de façon contrôlée une vulnérabilité",
                            "Analyser l'impact métier",
                            "Proposer une remédiation",
                            "Rédiger le rapport de pentest",
                        ],
                        "indices": [
                            "Sans autorisation écrite, on ne touche à rien : le scope précède toujours la technique.",
                            "Un rapport utile classe par criticité et donne une remédiation concrète à chaque finding.",
                            "Valider ne veut pas dire tout exploiter : preuve minimale d'impact suffit.",
                        ],
                        "criteres": [
                            "L'autorisation et le périmètre sont explicitement documentés",
                            "Au moins une vulnérabilité est validée par une preuve contrôlée",
                            "Chaque finding comporte criticité, impact et remédiation",
                            "Un rapport final structuré est produit",
                        ],
                        "mobilise": ["Pentest & rapport", "Reconnaissance en laboratoire", "Sécurité applicative web", "Analyse & détection d'incidents"],
                    },
                ],
            },
        ],
    },
]


# ----------------------------------------------------------------------------
# Fusion : base + missions supplémentaires + nouveau domaine Vision
# (les blocs « extra » réutilisent le même titre de domaine/compétence et
# viennent s'y greffer ; la commande seed fait des get_or_create.)
# ----------------------------------------------------------------------------
from cursus.content_python_extra import BLOCS as _PY_EXTRA  # noqa: E402
from cursus.content_reseaux_extra import BLOCS as _RESEAU_EXTRA  # noqa: E402
from cursus.content_cyber_extra import BLOCS as _CYBER_EXTRA  # noqa: E402
from cursus.content_vision import BLOCS as _VISION  # noqa: E402

CONTENU = CONTENU + _PY_EXTRA + _RESEAU_EXTRA + _CYBER_EXTRA + _VISION
