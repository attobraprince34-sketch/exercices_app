"""Générateur Cybersécurité — LABORATOIRE AUTORISÉ uniquement.

Tous les scénarios se déroulent sur des machines/vulns de labo fournies
(images légales, hashs d'entraînement, apps vulnérables volontaires).
Objectif affiché : comprendre la faille et la REMÉDIER. Outils gratuits.
"""

import random

from .base import contraintes, criteres, difficulte, duree, slug_unique

CADRAGE = (
    "CADRE LÉGAL : manipulation exclusivement sur le laboratoire fourni "
    "(machines isolées, hashs d'entraînement, applications vulnérables volontaires). "
    "Hors de ce périmètre, ces actes sont illégaux — l'objectif est de comprendre pour mieux défendre."
)

LABOS = ["Labo NetSec", "Cyber Range Académie", "Passerelle Sécurité", "Range Bleuet",
         "Atelier SOCÉcole", "Labo OpenFort", "Plateforme VulnÉco", "Range du Campus"]

FAMILLES = [
    {
        "id": "recon", "nom": "Reconnaissance & scan", "outils": "Nmap, Wireshark", "type": "laboratoire",
        "taches": [
            ("Inventaire des services ouverts",
             "Scanne la machine de labo {cible} et dresse l'inventaire des ports/services répondants."),
            ("Versions des services",
             "Récupère les versions banner des services de {cible} et liste ceux qui sont périmés."),
            ("Cartographier un sous-réseau",
             "Le labo {cible} cache {n} machines actives : découvre-les proprement et justifie tes options de scan."),
            ("Scan furtif vs bruyant",
             "Compare deux modes de scan sur {cible} : lesquels laissent des traces, lesquels donnent un résultat exploitable ?"),
            ("Vérifier une hypothèse de service",
             "On suppose que {cible} expose un service de gestion : confirme ou infirme avec un ciblage précis."),
        ],
    },
    {
        "id": "hash", "nom": "Analyse de mots de passe (hashs de labo)", "outils": "Hashcat / John the Ripper", "type": "laboratoire",
        "taches": [
            ("Reconnaître l'algo de hachage",
             "Le fichier {fichier} contient {n} hashs : identifie le ou les algorithmes utilisés."),
            ("Craquer un mot de passe faible",
             "Sur le hash d'entraînement {hash}, démontre avec une wordlist standard pourquoi ce MDP est cassable."),
            ("Test de robustesse d'une politique",
             "Évalue la politique MDP du labo : quels profils de mots de passe tiennent plus d'une heure ?"),
            ("Comparer salts et itérations",
             "Deux jeux de hashs du même MDP, deux configs : explique la différence de coût de cassage."),
            ("Remédiation : migrer le stockage",
             "Après avoir cassé les hashs faibles du labo, propose la config de hachage moderne qui les protègerait."),
        ],
    },
    {
        "id": "web", "nom": "Sécurité des apps web (labo)", "outils": "Navigateur + Burp Community (gratuit)", "type": "pentest",
        "taches": [
            ("SQLi sur formulaire de labo",
             "Le formulaire de connexion {cible} filtre mal les entrées : démontre l'injection puis écris la correction."),
            ("XSTored sur le livre d'or",
             "La page {cible}/galerie accepte du HTML non échappé : prouve le XSS stocké sur le labo, puis corrige le rendu."),
            ("CSRF sur le changement d'email",
             "Le profil {cible} ne valide pas de jeton : construis la preuve d'absence de protection et implémente le jeton."),
            ("IDOR sur les factures",
             "L'URL /facture/{n} laisse changer l'identifiant : teste l'accès non autorisé puis verrouille côté serveur."),
            ("Fuite d'infos par fichiers exposés",
             "Des fichiers de sauvegarde traînent sur {cible} : inventorie-les, évalue le risque et nettoie."),
        ],
    },
    {
        "id": "sys", "nom": "Durcissement système", "outils": "Linux de labo, Terminal", "type": "laboratoire",
        "taches": [
            ("Audit des permissions",
             "Sur la machine {cible}, repère les fichiers/exécutables aux permissions incorrectes et corrige-les sans rien casser."),
            ("Durcir SSH",
             "Le serveur {cible} autorise root+mot de passe : applique la politique recommandée et teste la bascule."),
            ("Comptes orphelins",
             "Le labo {cible} a {n} comptes dormants : inventorie, désactive et justifie chaque décision."),
            ("Service inutile = surface d'attaque",
             "Identifie les services qui tournent pour rien sur {cible}, arrête-les et mesure la surface gagnée."),
            ("Journalisation minimale",
             "Configure une journalisation exploitable sur {cible} : qui s'est connecté, quand, depuis où ?"),
        ],
    },
    {
        "id": "logs", "nom": "Analyse de logs & incident", "outils": "Linux, grep/awk ou Python", "type": "exercice",
        "taches": [
            ("Repérer un pic de connexions échouées",
             "Le fichier {fichier} couvre 24 h : détecte la fenêtre et la source de l'activité anormale."),
            ("Reconstituer une chronologie d'intrusion",
             "À partir des logs du labo {cible}, reconstitue le parcours de l'attaquant en une timeline."),
            ("Isoler une IP malveillante",
             "Une IP du fichier {fichier} a tenté {n} payloads différents : prouve-le et bloque-la."),
            ("Faux positifs",
             "Les alertes du labo signalent {cible} : démêle ce qui est un scan légitime d'une vraie attaque."),
            ("Rédiger un rapport d'incident",
             "Synthétise l'analyse de {fichier} en rapport : faits, impact, actions, recommandations."),
        ],
    },
    {
        "id": "phishing", "nom": "Hameçonnage & vigilance", "outils": "Client mail de labo, outils d'analyse texte", "type": "exercice",
        "taches": [
            ("Analyser un email suspect",
             "Le message {fichier} imite {domaine} : décortique en-têtes, liens et pièces, décris les indices."),
            ("Décanoter une URL",
             "Le lien reçu est raccourci en {n} sauts : reconstitue la destination réelle et le leurre."),
            ("Règles de détection",
             "Transforme tes indices en {n} règles simples applicables par toute l'équipe."),
            ("Sensibilisation",
             "Rédige la mini-note de vigilance illustrée par cet exemple de labo."),
            ("Signalement & conduite",
             "Définis la procédure : que faire quand un collaborateur a cliqué, sur la base du scénario {fichier} ?"),
        ],
    },
    {
        "id": "crypto", "nom": "Cryptographie appliquée", "outils": "Python / OpenSSL", "type": "exercice",
        "taches": [
            ("Stocker un MDP correctement",
             "Écris le script Python qui hache avec sel fort (hashlib) et vérifie une saisie."),
            ("Chiffrer un fichier sensible",
             "Protège {fichier} avec OpenSSL (AES) et produis la procédure d'accès pour l'équipe."),
            ("Générer des jetons",
             "Implémente des jetons aléatoires non devinables pour la réinitialisation de mot de passe."),
            ("Signature de livrables",
             "Signature un lot de {n} fichiers du labo et vérifie l'intégrité en chaîne."),
            ("Choisir le bon primitive",
             "Compare hachage/chiffrement/encodage sur un cas réel du labo et justifie tes choix."),
        ],
    },
]

CIBLES = ["10.0.0.10", "10.0.10.20", "lab-web-01", "lab-srv-02", "172.20.0.30", "vm-cible", "range-01", "10.10.40.50"]
FICHIERS = ["access.log", "auth.log", "hashes-labo.txt", "mails-suspects.eml", "capture.pcapng", "incident-2026-02.log"]
DOMAINES = ["banque-interne.fr", "rh-services.fr", "contact-assurance.fr", "service-publique.info"]
HASHS = ["$1$a5f3…", "$2b$12$Xq7…", "$6$salt$Rt9…", "5f4dcc3b5…"]


def _paliers(n, rng):
    pool = []
    for p in range(1, 11):
        pool.extend([p] * (4 if p <= 4 else 3))
    while len(pool) < n:
        pool.extend(pool)
    rng.shuffle(pool)
    return pool[:n]


def generer(n: int, graine: int = 13):
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
            "cible": rng.choice(CIBLES),
            "fichier": rng.choice(FICHIERS),
            "domaine": rng.choice(DOMAINES),
            "hash": rng.choice(HASHS),
            "n": rng.randint(2, 50),
        }
        titre = tache[0].format(**params)
        demande = tache[1].format(**params)
        labo = rng.choice(LABOS)

        contexte = f"{labo} met à disposition un environnement isolé pour cet exercice. {CADRAGE} Scénario : {demande}"
        probleme = (
            f"L'équipe {labo} doit prouver qu'elle comprend la faille ET sait la corriger : "
            f"{'analyse superficière ne suffit pas' if palier >= 5 else 'sans méthode, on passe à côté des vrais indices'}."
        )
        objectif = (
            f"Réaliser la mission sur le labo fourni : {titre.lower()}. "
            "Livrable : commande ou script exact, constats, et mesure de remédiation applicable en production."
        )
        environnement = f"Machine de labo isolée\nOutils : {fam['outils']}\nPérimètre strict : {params['cible']}, jamais au-delà"
        criteres_texte = criteres(
            f"Le résultat répond à la demande : {demande}",
            "Toute tentative hors du laboratoire est écartée et expliquée.",
            "Une mesure de correction concrète est proposée et justifiée pour chaque faille constatée.",
        )
        ce_que_tu_apprends = (
            f"{fam['nom']} en conditions défensives : comprendre l'attaque pour construire la protection. "
            f"Tu maîtrises : {demande}"
        )
        themes = f"{fam['id']},securite"
        if fam["id"] in {"web"}:
            themes += ",hacking,pentest"
        if palier >= 9:
            themes += ",projet"

        rows.append({
            "slug": slug_unique("cy", i, titre),
            "numero": 1,
            "titre": f"{fam['nom']} : {titre}"[:180],
            "accroche": f"{labo} — {demande}"[:200],
            "duree": duree(palier),
            "langage": "python" if fam["id"] in {"crypto", "logs"} else "texte",
            "outils": fam["outils"][:200],
            "palier": palier,
            "themes": themes,
            "type": fam["type"] if palier < 9 else "projet",
            "difficulte": diff,
            "contexte": contexte,
            "probleme": probleme,
            "objectif": objectif,
            "environnement": environnement,
            "contraintes": contraintes(palier),
            "amorce": f"# {titre}\n# Laboratoire autorisé : {params['cible']}\n# Rappel : comprendre puis remédier.\n",
            "ce_que_tu_apprends": ce_que_tu_apprends,
            "criteres_texte": criteres_texte,
            "ordre": palier,
            "publiee": True,
        })
    return rows
