"""Nouveau domaine : Vision par ordinateur (OpenCV / Python)."""

BLOCS = [
    {
        "domaine": {
            "titre": "Vision par ordinateur", "icone": "camera", "couleur": "orange", "ordre": 4,
            "sous_titre": "Analyser des images et des flux vidéo pour résoudre des problèmes concrets",
            "description": "Contrôle qualité, lecture de plaques, comptage, OCR, détection temps réel — avec OpenCV et Python.",
        },
        "competences": [
            {
                "titre": "Fondamentaux image avec OpenCV", "niveau": "debutant", "ordre": 1,
                "description": "Lire, comprendre et manipuler une image numérique.",
                "notions": [
                    {"titre": "Pixels & matrices", "resume": "Une image est un tableau de pixels ; en couleur, 3 canaux (BGR en OpenCV)."},
                    {"titre": "Lecture / écriture", "resume": "cv2.imread / imwrite / imshow : le trio de base."},
                    {"titre": "Espaces couleur", "resume": "BGR, RGB, gris, HSV — chaque espace sert un besoin d'analyse."},
                ],
                "missions": [
                    {
                        "numero": 1, "titre": "Convertir et normaliser un lot de photos d'archives",
                        "type": "exercice", "difficulte": "debutant", "langage": "python", "duree": "35 min",
                        "accroche": "Des milliers de photos hétérogènes : les mettre en niveaux de gris et à la même taille, automatiquement.",
                        "contexte": "Une médiathèque doit uniformiser des photos d'archives pour une base consultable.",
                        "probleme": "Formats et tailles variés rendent l'affichage et le stockage coûteux.",
                        "objectif": "Écrire un script qui convertit chaque image en niveaux de gris et la redimensionne.",
                        "environnement": "Python 3\nOpenCV (cv2)\nTerminal",
                        "contraintes": "Conserver le ratio (pas de déformation), éviter d'écraser les originaux.",
                        "etapes": [
                            "Lire une image (cv2.imread)",
                            "Convertir en niveaux de gris (cvtColor)",
                            "Redimensionner en gardant le ratio",
                            "Sauvegarder dans un dossier de sortie",
                            "Traiter tout un dossier en boucle",
                        ],
                        "indices": [
                            "cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) passe en gris.",
                            "cv2.resize avec interpolation pour conserver la qualité.",
                        ],
                        "criteres": [
                            "Les images de sortie sont en niveaux de gris",
                            "La largeur cible est respectée sans déformation",
                            "Les originaux restent intacts",
                        ],
                        "amorce": "import cv2, glob, os\n\nENTREE='archives'\nSORTIE='normalise'\nLARGEUR=640\n\ndef normaliser(img):\n    ...\n",
                        "mobilise": ["Fondamentaux image avec OpenCV"],
                    },
                ],
            },
            {
                "titre": "Prétraitement d'images", "niveau": "intermediaire", "ordre": 2,
                "description": "Bruit, flou, seuillage : préparer l'image avant de l'analyser.",
                "notions": [
                    {"titre": "Filtrage / flou", "resume": "Gaussian blur réduit le bruit avant détection."},
                    {"titre": "Seuillage", "resume": "threshold / Otsu sépare l'objet du fond."},
                    {"titre": "Détection de contours", "resume": "Canny fait ressortir les arêtes utiles aux contours."},
                ],
                "missions": [
                    {
                        "numero": 1, "titre": "Préparer une image de radiographie pour un contrôle",
                        "type": "exercice", "difficulte": "intermediaire", "langage": "python", "duree": "50 min",
                        "accroche": "Une pièce est-elle fissurée ? Il faut d'abord débruiter et segmenter l'image.",
                        "contexte": "Un atelier de contrôle non destructif analyse des images de pièces métalliques.",
                        "probleme": "Le bruit et l'éclairage inégal masquent les défauts.",
                        "objectif": "Construire une chaîne de prétraitement réutilisable (flou + seuillage + contours).",
                        "environnement": "Python 3\nOpenCV",
                        "contraintes": "Fonctions enchaînables, paramètre de seuil testé, pas de perte de la zone d'intérêt.",
                        "etapes": [
                            "Charger l'image en niveaux de gris",
                            "Appliquer un flou gaussien (débruitage)",
                            "Seuiller (Otsu) pour isoler la pièce",
                            "Extraire les contours (Canny)",
                            "Assembler en une fonction pipeline()",
                        ],
                        "indices": [
                            "cv2.GaussianBlur((5,5)) avant tout seuillage.",
                            "cv2.threshold(..., cv2.THRESH_BINARY+cv2.THRESH_OTSU) automatise le seuil.",
                        ],
                        "criteres": [
                            "Le bruit est nettement réduit",
                            "La pièce est segmentée du fond",
                            "Les contours sont exploitables",
                        ],
                        "amorce": "import cv2\n\ndef pipeline(path):\n    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)\n    # flou -> seuillage -> canny\n    return ...\n",
                        "mobilise": ["Prétraitement d'images", "Fondamentaux image avec OpenCV"],
                    },
                ],
            },
            {
                "titre": "Détection de formes & contours", "niveau": "intermediaire", "ordre": 3,
                "description": "Repérer, compter et mesurer des objets dans une image.",
                "notions": [
                    {"titre": "Contours", "resume": "cv2.findContours isole les objets pour les analyser."},
                    {"titre": "Approximation poly", "resume": "approxPolyDP permet de reconnaître rectangles/triangles."},
                    {"titre": "Enclos & aire", "resume": "boundingRect / minAreaRect pour mesurer et localiser."},
                ],
                "missions": [
                    {
                        "numero": 1, "titre": "Compter des pièces sur un convoyeur",
                        "type": "projet", "difficulte": "intermediaire", "langage": "python", "duree": "1 h",
                        "accroche": "Combien de pièces passent sur la photo ? Détection et comptage automatiques.",
                        "contexte": "Une ligne de production photographié le convoyeur ; le comptage manuel est fatigant et sujet à erreur.",
                        "probleme": "Il faut dénombrer les pièces et repérer celles qui se chevauchent anormalement.",
                        "objectif": "Détecter les objets, les compter et annoter l'image de contrôle.",
                        "environnement": "Python 3\nOpenCV",
                        "contraintes": "Filtrer le bruit (trop petits objets), marquer chaque pièce détectée, produire le compte.",
                        "etapes": [
                            "Segmenter les pièces du fond (seuillage)",
                            "Extraire les contours",
                            "Filtrer par aire minimale",
                            "Dessiner un enclos sur chaque pièce",
                            "Afficher le nombre détecté",
                        ],
                        "indices": [
                            "cv2.contourArea(c) pour ignorer les pixels isolés.",
                            "cv2.boundingRect donne la boîte englobante à dessiner.",
                        ],
                        "criteres": [
                            "Le compte correspond aux pièces visibles",
                            "Le bruit est ignoré (pas de faux positifs minimes)",
                            "L'image annotée est enregistrée",
                        ],
                        "amorce": "import cv2\n\ndef compter(path):\n    img = cv2.imread(path)\n    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)\n    # seuillage -> findContours -> filtrer aie -> dessiner\n",
                        "mobilise": ["Détection de formes & contours", "Prétraitement d'images"],
                    },
                    {
                        "numero": 2, "titre": "Contrôle qualité : détecter une forme défectueuse",
                        "type": "exercice", "difficulte": "intermediaire", "langage": "python", "duree": "45 min",
                        "accroche": "Rejeter la pièce dont la forme ne correspond pas au gabarit.",
                        "contexte": "Une caméra photographie chaque pièce ; l'appariement de forme permet de rejeter les anomalies.",
                        "probleme": "Des pièces déformées passent le contrôle visuel humain.",
                        "objectif": "Comparer la forme détectée à un gabarit et signaler les écarts.",
                        "environnement": "Python 3\nOpenCV",
                        "contraintes": "Seuil de tolérance défini, décision conforme/non conforme claire.",
                        "etapes": [
                            "Extraire le contour principal",
                            "Calculer un descripteur de forme (circularité / approxPolyDP)",
                            "Comparer au gabarit de référence",
                            "Étiqueter conforme / non conforme",
                        ],
                        "indices": [
                            "Circularité = 4*pi*aire / perimetre^2 (1 = cercle parfait).",
                            "matchShapes compare deux contours.",
                        ],
                        "criteres": [
                            "Une pièce normale est acceptée",
                            "Une pièce déformée est rejetée",
                            "Le seuil de tolérance est explicite",
                        ],
                        "amorce": "import cv2, math\n\ndef conforme(contour):\n    aire = cv2.contourArea(contour)\n    per = cv2.arcLength(contour, True)\n    circularite = 4*math.pi*aire/(per*per) if per else 0\n    return ...\n",
                        "mobilise": ["Détection de formes & contours"],
                    },
                ],
            },
            {
                "titre": "Reconnaissance & OCR", "niveau": "avance", "ordre": 4,
                "description": "Faire lire du texte à la machine.",
                "notions": [
                    {"titre": "Segmentation de texte", "resume": "Isoler les caractères/lignes avant la reconnaissance."},
                    {"titre": "OCR (Tesseract)", "resume": "Convertir une zone d'image en texte exploitable."},
                ],
                "missions": [
                    {
                        "numero": 1, "titre": "Lire une plaque d'immatriculation pour un parking",
                        "type": "projet", "difficulte": "avance", "langage": "python", "duree": "1 h 30",
                        "accroche": "Barrière automatique : détecter la plaque puis la lire.",
                        "contexte": "Un parking veut ouvrir la barrière en lisant automatiquement la plaque depuis une image.",
                        "probleme": "La plaque est petite, parfois inclinée, sur un arrière-plan occupé.",
                        "objectif": "Localiser la zone de la plaque, la redresser, puis extraire le texte par OCR.",
                        "environnement": "Python 3\nOpenCV\nTesseract (pytesseract)\nLABORATOIRE / IMAGES D'EXEMPLE",
                        "contraintes": "Utiliser des images d'exemple fournies ; aucune donnée personnelle réelle.",
                        "etapes": [
                            "Prétraiter l'image (gris, flou, seuillage)",
                            "Détecter la région candidate de la plaque",
                            "Extraire et redresser la zone",
                            "Lancer l'OCR (pytesseract)",
                            "Nettoyer et valider le format du texte",
                        ],
                        "indices": [
                            "Un rectangle allongé de ratio ~ 4:1 est un bon candidat plaque.",
                            "pytesseract.image_to_string avec un config de whitelist accélère le résultat.",
                        ],
                        "criteres": [
                            "La zone plaque est correctement isolée",
                            "Le texte OCR correspond à la plaque d'exemple",
                            "Le résultat est validé par un format attendu",
                        ],
                        "amorce": "import cv2, pytesseract\n\n# image d'exemple fournie (pas de donnée réelle)\ndef lire_plaque(path):\n    ...\n",
                        "mobilise": ["Reconnaissance & OCR", "Prétraitement d'images", "Détection de formes & contours"],
                    },
                ],
            },
            {
                "titre": "Vision temps réel (caméra)", "niveau": "avance", "ordre": 5,
                "description": "Traiter un flux vidéo en direct.",
                "notions": [
                    {"titre": "Boucle vidéo", "resume": "read -> traitement -> affichage, image par image."},
                    {"titre": "Détection dans une frame", "resume": "Appliquer une détection à chaque image du flux."},
                    {"titre": "Suivi simple", "resume": "Repérer un objet en mouvement (soustraction de fond)."},
                ],
                "missions": [
                    {
                        "numero": 1, "titre": "Détecter le port du casque sur un chantier (simulation)",
                        "type": "projet", "difficulte": "expert", "langage": "python", "duree": "2 h",
                        "accroche": "Flux caméra simulé : alerter quand une zone de sécurité n'est pas respectée.",
                        "contexte": "Sur un chantier, une caméra (flux d'exemple/simulation) doit aider à la sécurité.",
                        "probleme": "Le respect du port des équipements n'est pas vérifié en continu.",
                        "objectif": "Mettre en place une boucle de vision temps réel qui signale une anomalie.",
                        "environnement": "Python 3\nOpenCV\nModèle de détection (ex. Haar/ONNX)\nImages/vidéo d'EXEMPLE",
                        "contraintes": "Travailler sur une vidéo d'exemple, pas sur des personnes réelles sans consentement. Latence maîtrisée.",
                        "etapes": [
                            "Ouvrir la vidéo d'exemple (VideoCapture)",
                            "Charger un détecteur (cascade / modèle)",
                            "Détecter les zones pertinentes image par image",
                            "Déclencher une alerte visuelle en cas de manquement",
                            "Mesurer la fluidité (FPS)",
                        ],
                        "indices": [
                            "cv2.VideoCapture(0) pour caméra, un path pour une vidéo d'exemple.",
                            "cascade_detector.detectMultiScale localise les objets.",
                        ],
                        "criteres": [
                            "La boucle tourne sur la vidéo d'exemple",
                            "Une détection est affichée en temps quasi réel",
                            "Une alerte visuelle se déclenche correctement",
                        ],
                        "amorce": "import cv2\n\ncap = cv2.VideoCapture('exemple_chantier.mp4')  # vidéo d'EXEMPLE\nwhile cap.isOpened():\n    ok, frame = cap.read()\n    if not ok: break\n    # detection + annotation\n",
                        "mobilise": ["Vision temps réel (caméra)", "Détection de formes & contours", "Prétraitement d'images"],
                    },
                ],
            },
        ],
    },
]
