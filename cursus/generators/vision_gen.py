"""Générateur Vision par ordinateur : OpenCV en Python, projets image/vidéo.

Paliers bas : manipulation d'images uniques. Paliers hauts : flux vidéo,
robustesse, petits systèmes de vision complets.
"""

import random

from .base import contraintes, criteres, difficulte, duree, slug_unique

CONTEXTES = [
    ("atelier de production", "tri de pièces sur convoyeur", "caméra fixe au-dessus du tapis"),
    ("parking", "comptage de places libres", "caméra d'entrée de parking"),
    ("dépôt logistique", "lecture d'étiquettes", "caméra sur potence"),
    ("serre agricole", "surveillance de l'état des plantes", "caméra sur rail"),
    ("laboratoire", "analyse de lames au microscope", "microscope numérique"),
    ("imprimerie", "contrôle qualité d'impression", "caméra linéaire"),
    ("commerce", "file d'attente en caisse", "caméra d'ambiance"),
    ("portique de saisie", "reconnaissance de plaques", "caméra de passage"),
    ("salle de sport", "comptage de mouvements", "caméra grand angle"),
    ("musée", "flux de visiteurs", "caméra d'entrée"),
    ("cantine", "comptage des plateaux", "caméra de ligne"),
    ("copropriété", "relevé de compteurs", "caméra sur support"),
    ("centre de tri", "détection d'objets sur bande", "caméra zénithale"),
    ("élevage", "détection d'animaux au portail", "caméra extérieure"),
    ("scierie", "comptage de planches", "caméra de fin de ligne"),
]

SOURCES = ["image 'entree.png'", "image 'planche.jpg'", "dossier d'images 'lot_01/'",
           "vidéo 'cam.mp4' (30 ips)", "flux webcam 0", "images scannées en TIFF"]

FAMILLES = [
    {
        "id": "bases", "nom": "Bases & manipulation", "apps": "charger, convertir, afficher et sauvegarder une image proprement.",
        "taches": [
            ("Redimensionner et convertir", "Charge {source}, ramène-le à {w}x{h} puis en niveaux de gris, et sauvegarde le résultat."),
            ("ROI : zone d'intérêt", "Extrais de {source} la zone (x={x}, y={y}, {w}x{h}) et reconstruis une image propre à partir de ce recadrage."),
            ("Rotations et retournements", "Produis à partir de {source} les {n} variantes d'orientation attendues par l'étape suivante."),
            ("Histogramme et luminosité", "Calcule l'histogramme de {source} et corrige la luminosité des images trop sombres du lot."),
            ("Dessiner par-dessus", "Annote {source} avec rectangles, flèches et légende pour préparer le dossier de contrôle."),
        ],
    },
    {
        "id": "seuillage", "nom": "Seuillage & binarisation", "apps": "séparer le premier plan de l'arrière-plan de façon robuste.",
        "taches": [
            ("Seuil simple vs Otsu", "Binarise {source} par seuil fixe puis par Otsu ; compare et choisis avec des critères mesurables."),
            ("Seuillage adaptatif", "Les éclairages varient sur {source} : applique un seuillage adaptatif qui tient compte des ombres."),
            ("Compter les objets binarisés", "Après binarisation de {source}, compte les composantes connexes de taille > {min_px} pixels."),
            ("Nettoyer le bruit", "Élimine le pointillisme post-seuillage (ouvertures/fermetures) sans effacer les petits objets."),
            ("Seuil couleur (HSV)", "Isole dans {source} les pixels d'une teinte précise via une conversion HSV et leurs bornes."),
        ],
    },
    {
        "id": "contours", "nom": "Contours & formes", "apps": "extraire la géométrie des objets : contour, aire, périmètre, approximation.",
        "taches": [
            ("Trouver et dessiner les contours", "Détecte les contours de {source}, hiérarchise-les et dessine-les avec leur index."),
            ("Trier par aire", "Classe les formes de {source} par aire décroissante et signale celles qui sortent de la tolérance (< {min_px} px)."),
            ("Approximation polygonale", "Reconnais les polygones de {source} par approximation epsilon et étiquette-les (triangle, rectangle, autre)."),
            ("Cercles et rectangles", "Distingue cercles et rectangles dans {source} par critères géométriques, avec taux de confiance."),
            ("Min-area rect sur pivot", "Pour les pièces penchées de {source}, calcule le rectangle tournant minimal et ses dimensions."),
        ],
    },
    {
        "id": "comptage", "nom": "Comptage & mesure", "apps": "transformer une image en chiffres fiables : comptage, taille, distance.",
        "taches": [
            ("Compter sur le tapis", "Sur {source}, compte les objets et produis le total ainsi que la liste des surfaces."),
            ("Mesurer en pixels puis en mm", "Étalonne {source} avec un référent connu de {w} px, puis mesure le diamètre des objets en mm."),
            ("Comptage vidéo", "Sur {source} vidéo, comptabilise les passages d'objets par la ligne virtuelle en gérant le double comptage."),
            ("Moyenne mobile de comptage", "Lisse la série de comptages du lot et alerte quand un écart dépasse {min_px}%."),
            ("Densité par zone", "Cartographie la densité d'objets par quadrant sur {source} et exporte le tableau."),
        ],
    },
    {
        "id": "filtrage", "nom": "Filtres & amélioration", "apps": "préparer l'image pour une étape de vision : flou, bruit, contours.",
        "taches": [
            ("Flou et bruit", "Compare flou gaussien/médian sur {source} bruitée : quantifie lequel préserve les bords à {w} px."),
            ("Détection de Canny", "Règle les seuils de Canny sur {source} pour extraire les arêtes utiles au contrôle."),
            ("Érode / dilater", "Utilise la morphologie pour combler les trous et isoler les formes de {source}."),
            ("Réhaussement local", "Améliore le contraste local de {source} (CLAHE) pour la suite de traitement."),
            ("Inpainting de défauts", "Masque les taches du lot {source} et reconstruis l'image avant analyse."),
        ],
    },
    {
        "id": "ocr", "nom": "OCR & texte", "apps": "faire parler le texte des images : extraction, nettoyage, contrôle.",
        "taches": [
            ("OCR d'étiquette", "Extrais le texte de {source} (pytesseract) et reconstruis les champs ref/quantité."),
            ("OCR en lot", "Traite {source} de lot, produis un CSV (ref, texte, confiance) avec seuil de rejet."),
            ("Pré-traitement pour OCR", "Améliore le taux de reconnaissance de {source} par binarisation + déformation corrigée."),
            ("Plaque : découpe et lecture", "Localise la zone probable de plaque dans {source}, redresse-la puis passe l'OCR."),
            ("Contrôle de champs", "Valide le résultat OCR de {source} contre un motif (regex) et liste les rejets."),
        ],
    },
    {
        "id": "video", "nom": "Vidéo & mouvement", "apps": "analyser des flux : différence de fond, suivi, événements.",
        "taches": [
            ("Soustraction de fond", "Sur {source} vidéo, isole les objets en mouvement par soustraction d'arrière-plan."),
            ("Suivi d'objet simple", "Suis l'objet détecté cadre à cadre (centre + vitesse) et exporte sa trajectoire en CSV."),
            ("Déclencheur d'événement", "Déclenche une alerte quand {n} objets franchissent la ligne sur {source}."),
            ("Stabilisation", "Compense les micro-tremblements de {source} avant toute mesure."),
            ("Extraction d'images", "Échantillonne {source} (1 image sur {n}) pour constituer le lot d'analyse."),
        ],
    },
]

def _paliers(n, rng):
    pool = []
    for p in range(1, 11):
        pool.extend([p] * (4 if p <= 4 else 3))
    while len(pool) < n:
        pool.extend(pool)
    rng.shuffle(pool)
    return pool[:n]


def generer(n: int, graine: int = 21):
    rng = random.Random(graine)
    rows = []
    paliers = _paliers(n, rng)
    combos = [(fam, tache) for fam in FAMILLES for tache in fam["taches"]]
    rng.shuffle(combos)

    for i in range(n):
        fam, tache = combos[i % len(combos)]
        palier = paliers[i]
        diff = difficulte(palier)
        ctx = rng.choice(CONTEXTES)
        params = {
            "source": rng.choice(SOURCES),
            "w": rng.choice([320, 480, 640, 800]),
            "h": rng.choice([240, 360, 480, 600]),
            "x": rng.randint(10, 200),
            "y": rng.randint(10, 150),
            "n": rng.randint(2, 20),
            "min_px": rng.choice([20, 50, 120, 250]),
        }
        titre = tache[0].format(**params)
        demande = tache[1].format(**params)

        contexte = (
            f"Dans un {ctx[0]}, la mission « {ctx[1]} » s'appuie sur une {ctx[2]}. "
            f"Les images arrivent sans garantie de qualité : à ton programme de tenir la route. Scénario : {demande}"
        )
        constat = "est encore fait à l'œil" if palier <= 4 else "actuel se plante dès que la lumière change"
        probleme = (
            f"Le contrôle {constat} : "
            "il faut un traitement d'image reproductible et chiffré."
        )
        objectif = (
            f"Écrire un script Python/OpenCV qui réalise : {titre.lower()}. "
            f"Afficher/sauvegarder les images intermédiaires et imprimer le résultat attendu."
        )
        environnement = f"Python 3 + OpenCV\nVS Code\nContexte : {ctx[0]} ({ctx[2]})"
        criteres_texte = criteres(
            f"Le script produit le résultat décrit : {demande}",
            "Les images de contrôle intermédiaires sont sauvegardées et regardables.",
            "Le script tourne aussi sur une image du lot plus difficile (ombre/bruit).",
        )
        ce_que_tu_apprends = (
            f"{fam['nom']} : {fam['apps']} Tu maîtrises : {demande}"
        )
        themes = f"{fam['id']},cv"
        if palier >= 9:
            themes += ",projet"

        rows.append({
            "slug": slug_unique("cv", i, titre),
            "numero": 1,
            "titre": f"{fam['nom']} : {titre}"[:180],
            "accroche": f"{ctx[0].capitalize()} — {demande}"[:200],
            "duree": duree(palier),
            "langage": "python",
            "outils": "Python / OpenCV / VSCode",
            "palier": palier,
            "themes": themes,
            "type": "projet" if palier >= 9 else "exercice",
            "difficulte": diff,
            "contexte": contexte,
            "probleme": probleme,
            "objectif": objectif,
            "environnement": environnement,
            "contraintes": contraintes(palier),
            "amorce": f"# {titre}\nimport cv2\n\nimage = cv2.imread('entree.png')\n# TODO : {demande[:90]}\n",
            "ce_que_tu_apprends": ce_que_tu_apprends,
            "criteres_texte": criteres_texte,
            "ordre": palier,
            "publiee": True,
        })
    return rows
