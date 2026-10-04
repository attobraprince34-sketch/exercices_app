"""Générateur Python pur : mises en situation de traitement de données réelles.

Combinatoire : métier (données réelles) × famille technique × opération × palier.
Chaque exercice reste écrit en français naturel avec données d'entrée,
résultat attendu et critères de réussite testables.
"""

import random

from .base import contraintes, criteres, difficulte, duree, slug_unique

ENTREPRISES = [
    "Boutique Éclat", "Transports LogiFast", "Menuiserie Dubois", "Cabinet ComptaNet",
    "Ferme des Tilleuls", "Studio Pixel", "Clinique VétAll", "Agence VoyageLoin",
    "Garage Vitamoteur", "Boulangerie du Marché", "Librairie Pages", "Start-up PayFlow",
    "Atelier Fil Rouge", "Salle de sport Forme+", "Syndic ImmoCare", "École Les Pléiades",
    "Restaurant Saveurs", "Pharmacie Centrale", "Imprimerie RectoVerso", "Entrepôt Stock3000",
    "Cabinet Juridice", "Association RéseauSolidaire", "Pressing Netto", "Fleuriste Pétales",
    "Atelier Vélo+", "Courtier AssurPro", "Fabricant PetFood", "Conciergerie SleepWell",
    "Scierie TraitBois", "Cave du Cep",
]

# (nom du jeu de données, entité, description des enregistrements, exemples de champs)
METIERS = [
    ("les factures", "facture", "un export comptable", "montant, date, client, payée"),
    ("les commandes clients", "commande", "le journal des ventes en ligne", "id, client, articles, total, statut"),
    ("les fiches de paie", "salarié", "la paie mensuelle", "nom, base, primes, taux, net"),
    ("les logs du serveur", "ligne de log", "un fichier journal brut", "horodatage, niveau, message, ip"),
    ("les votes d'une élection interne", "vote", "un bureau de vote", "electeur, candidat, region"),
    ("les résultats du dernier quiz", "réponse", "un questionnaire en ligne", "candidat, question, points"),
    ("le carnet d'adresses", "contact", "un fichier de contacts", "nom, telephone, email, ville"),
    ("les relevés bancaires", "mouvement", "un relevé CSV", "date, libelle, montant, categorie"),
    ("les plannings des équipes", "créneau", "le tableau de service", "agent, jour, debut, fin, service"),
    ("les tickets de support", "ticket", "la file d'assistance", "ref, priorite, statut, agent, délai"),
    ("les articles du catalogue", "produit", "un export e-commerce", "ref, nom, prix, stock, categorie"),
    ("les notes des élèves", "élève", "un cahier de notes", "nom, matiere, note, coef"),
    ("les relevés de capteurs d'atelier", "mesure", "des sondeurs qui télémétrent", "capteur, valeur, unite, horodatage"),
    ("les playlists de la radio interne", "titre", "une base musicale", "titre, artiste, duree, genre"),
    ("les recettes de production", "ingrédient", "un ordonnancement cuisine", "recette, ingredient, quantite, unite"),
    ("les dépenses de l'année", "dépense", "un suivi budgétaire", "date, poste, montant, responsable"),
    ("les abonnés du service", "abonnement", "une base clients", "client, plan, debut, renouvellement, actif"),
    ("les patients du cabinet", "patient", "un fichier de rendez-vous anonymisé", "id, age, medecin, motif, date"),
    ("les incidents enregistrés", "incident", "un registre d'incidents", "ref, gravite, service, duree, resolu"),
    ("les articles du blog", "article", "une liste de publications", "titre, auteur, mots, date, tags"),
    ("les commentaires modérés", "commentaire", "une file de modération", "auteur, texte, signalement, note"),
    ("les adresses des clients", "adresse", "un fichier de livraison", "rue, code_postal, ville, pays"),
    ("les hachages de test", "hash", "un échantillon de laboratoire", "algo, hash, indicatif"),
    ("les emails de la boîte partagée", "email", "un export de messagerie", "expediteur, objet, date, lu"),
    ("les URL du site", "lien", "un crawler interne", "url, statut, temps_reponse, section"),
    ("l'inventaire du magasin", "article", "un comptage stock", "ref, designation, quantite, seuil"),
    ("les virements de la semaine", "virement", "un fichier de remise en banque", "reference, montant, emitte, recu"),
    ("les créneaux de livraison", "livraison", "un plan de tournée", "tournee, ville, colis, poids, priorite"),
    ("les pointages du personnel", "pointage", "des badges d'entrée/sortie", "matricule, date, entree, sortie"),
    ("les documents numérisés", "document", "une GED d'archives", "ref, type, annee, taille, auteur"),
]

FAMILLES = [
    {"id": "types", "nom": "Variables & types", "apps": "Manipuler des types et les convertir sans perdre d'information."},
    {"id": "chaine", "nom": "Chaînes de caractères", "apps": "Nettoyer, normaliser et reformater du texte réel."},
    {"id": "liste", "nom": "Listes & boucles", "apps": "Parcourir et transformer un lot d'enregistrements."},
    {"id": "dict", "nom": "Dictionnaires", "apps": "Modéliser une entité métier avec des clés lisibles."},
    {"id": "fonction", "nom": "Fonctions", "apps": "Isoler une opération réutilisable et testable."},
    {"id": "tri", "nom": "Tri & comparaison", "apps": "Ordonner selon plusieurs critères métier."},
    {"id": "recherche", "nom": "Recherche", "apps": "Retrouver vite une information dans un gros volume."},
    {"id": "fichier", "nom": "Fichiers & CSV", "apps": "Lire et produire des fichiers utilisés par d'autres outils."},
    {"id": "json", "nom": "JSON", "apps": "Intervertir données structurées et texte."},
    {"id": "regex", "nom": "Expressions régulières", "apps": "Reconnaître et extraire des motifs (emails, codes, dates)."},
    {"id": "dates", "nom": "Dates & horaires", "apps": "Exploiter des horodatages et calculer des durées."},
    {"id": "oop", "nom": "Classes & objets", "apps": "Structurer un petit domaine métier en objets."},
    {"id": "erreur", "nom": "Gestion des erreurs", "apps": "Rendre un script fiable face aux données sales."},
    {"id": "set", "nom": "Ensembles & déduplication", "apps": "Éliminer les doublons et comparer des collections."},
    {"id": "comprehension", "nom": "Comprehensions", "apps": "Écrire des transformations concises et claires."},
    {"id": "itertools", "nom": "Itertools", "apps": "Agréger des séquences sans y penser à deux fois."},
    {"id": "matrice", "nom": "Matrices 2D", "apps": "Traiter des tableaux (grilles, plannings, images)."},
    {"id": "recursif", "nom": "Récursivité", "apps": "Résoudre un problème qui s'appelle lui-même."},
]

OPERATIONS = [
    {"id": "filtrer", "demande": "ne conserver que les {entite}s qui respectent une règle métier précise",
     "crit": "Seuls les {entite}s validant la règle sont conservés."},
    {"id": "trier", "demande": "trier les {entite}s selon deux critères superposables (principal puis secondaire)",
     "crit": "L'ordre de tri respecte les deux critères, y compris en cas d'égalité."},
    {"id": "agreger", "demande": "calculer la somme, la moyenne et le maximum sur un champ numérique des {entite}s",
     "crit": "Les trois agrégats sont exacts sur le jeu d'exemple."},
    {"id": "compter", "demande": "compter les {entite}s par catégorie et désigner la catégorie dominante",
     "crit": "Le comptage par catégorie est exhaustif et sans double compte."},
    {"id": "grouper", "demande": "regrouper les {entite}s par clé et produire un résumé par groupe",
     "crit": "Chaque {entite} appartient à un seul groupe ; les totaux par groupe sont justes."},
    {"id": "dedup", "demande": "débarrasser le jeu de {entite}s de ses doublons",
     "crit": "Aucun doublon ne subsiste et les éléments uniques sont préservés."},
    {"id": "transformer", "demande": "transformer chaque {entite} brute en une {entite} normalisée prête pour un autre outil",
     "crit": "La sortie a le format demandé et toutes les {entite}s sont converties."},
    {"id": "valider", "demande": "vérifier la validité de chaque {entite} et produire un rapport des rejets motivés",
     "crit": "Toutes les {entite}s invalides sont détectées avec une raison explicite."},
    {"id": "rechercher", "demande": "retrouver les {entite}s correspondant à une requête multicritère",
     "crit": "La recherche renvoie les bonnes {entite}s, y compris sans accent et en casse mixte."},
    {"id": "formater", "demande": "générer un document de synthèse lisible à partir des {entite}s",
     "crit": "Le document reprend l'ensemble des {entite}s avec un formatage constant."},
    {"id": "convertir", "demande": "convertir les {entite}s d'un format vers un autre sans perte",
     "crit": "La conversion est fidèle dans les deux sens sur le jeu d'exemple."},
]

EXTRA_PALEMENT = [
    "Le responsable veut un résultat vérifiable en moins de deux minutes.",
    "Données reçues chaque matin, format parfois capricieux.",
    "Le script remplacera une saisie manuelle source d'erreurs.",
    "Un collègue doit pouvoir reprendre le code sans explication.",
    "Volume en croissance : le traitement doit rester simple.",
    "La direction réclame un export propre pour la comptabilité.",
    "Une erreur de traitement a déjà été détectée le mois dernier.",
    "L'outil tourne en local, sans accès à Internet.",
]


def _paliers(n: int, rng: random.Random):
    """Répartit les paliers 1..10 de façon équilibrée, un peu plus de bases."""
    pool = []
    for p in range(1, 11):
        pool.extend([p] * (4 if p <= 4 else 3))
    while len(pool) < n:
        pool.extend(pool)
    rng.shuffle(pool)
    return pool[:n]


def generer(n: int, graine: int = 42):
    rng = random.Random(graine)
    rows = []
    combos = [
        (metier, famille, op)
        for metier in METIERS
        for famille in FAMILLES
        for op in OPERATIONS
    ]
    rng.shuffle(combos)
    paliers = _paliers(n, rng)

    for i in range(n):
        metier, famille, op = combos[i % len(combos)]
        palier = paliers[i]
        diff = difficulte(palier)
        entreprise = rng.choice(ENTREPRISES)
        # Construction des textes.
        entite = metier[1]
        donnees = metier[2]
        champs = metier[3]
        demande = op["demande"].format(entite=entite)
        consigne = EXTRA_PALEMENT[rng.randrange(len(EXTRA_PALEMENT))]
        supcontexte = EXTRA_PALEMENT[rng.randrange(len(EXTRA_PALEMENT))]
        while supcontexte == consigne:
            supcontexte = EXTRA_PALEMENT[rng.randrange(len(EXTRA_PALEMENT))]

        titre = f"{famille['nom']} : {op['id'].capitalize()} — {metier[0]}"
        if palier >= 7:
            titre += f" (volume important)"
        accroche = f"Chez {entreprise}, {donnees} ({champs}) : {demande}."

        contexte = (
            f"{entreprise} manipule {donnees} ({champs}). {supcontexte} "
            f"Les enregistrements arrivent en vrac et doivent être exploitables rapidement."
        )
        probleme = (
            f"Aujourd'hui, {op['demande'].format(entite=entite)} se fait à la main ou dans un tableur, "
            f"avec erreurs et reprises permanentes."
        )
        objectif = (
            f"Écrire un programme Python qui charge {donnees} et qui doit {demande}. "
            f"Fonction attendue : traiter(enregistrements) -> resultat. "
            f"Afficher le résultat au format texte."
        )
        environnement = f"Python 3\nVS Code\nTerminal\nJeu de données d'exemple : {champs}"
        criteres_texte = criteres(op["crit"].format(entite=entite),
                                  f"Le programme indique clairement s'il reste des {entite}s non traitées.")
        ce_que_tu_apprends = (
            f"{famille['nom']} en pratique : {famille['apps']} "
            f"Tu maîtrises : {demande} sur des données réelles."
        )
        themes = f"{famille['id']},data"
        if palier >= 9:
            themes += ",projet"

        rows.append({
            "slug": slug_unique("py", i, titre),
            "numero": 1,
            "titre": titre[:180],
            "accroche": accroche[:200],
            "duree": duree(palier),
            "langage": "python",
            "outils": "Python / VSCode",
            "palier": palier,
            "themes": themes,
            "type": "projet" if palier >= 9 else "exercice",
            "difficulte": diff,
            "contexte": contexte,
            "probleme": probleme,
            "objectif": objectif,
            "environnement": environnement,
            "contraintes": contraintes(palier),
            "amorce": f"# {titre}\n# Données d'exemple : {champs}\n\ndef traiter(enregistrements):\n    ...\n",
            "ce_que_tu_apprends": ce_que_tu_apprends,
            "criteres_texte": criteres_texte,
            "ordre": palier,
            "publiee": True,
        })
    return rows
