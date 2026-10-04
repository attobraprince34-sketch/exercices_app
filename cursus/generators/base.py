"""Outils partagés par les générateurs d'exercices.

Chaque générateur de domaine expose : generer(n, graine) -> list[dict]
Les dicts contiennent les champs de `Mission` (sans `domaine`, ajouté par la
commande) + un `slug` déterministe et unique.
"""

PALIERS = list(range(1, 11))

DUREES = ["15 min", "20 min", "25 min", "30 min", "35 min",
          "45 min", "50 min", "1 h", "1 h 15", "1 h 30"]

_DIFFICULTE = [(1, 3, "debutant"), (4, 6, "intermediaire"), (7, 8, "avance"), (9, 10, "expert")]


def difficulte(palier: int) -> str:
    for lo, hi, label in _DIFFICULTE:
        if lo <= palier <= hi:
            return label
    return "debutant"


def duree(palier: int) -> str:
    return DUREES[min(max(palier, 1), 10) - 1]


# Contraintes « professionnelles » proportionnées au palier.
CONTRAINTES = {
    "debutant": [
        "Code lisible, noms de variables explicites.",
        "Aucune bibliothèque externe : uniquement la standard library.",
        "Le programme doit tourner sans erreur sur le jeu de données d'exemple.",
    ],
    "intermediaire": [
        "Aucune bibliothèque externe non justifiée.",
        "Gérer les entrées manquantes ou invalides sans planter.",
        "Découper le traitement en fonctions courtes et testables.",
    ],
    "avance": [
        "Traiter un volume important : éviter les boucles imbriquées inutiles.",
        "Gérer les cas limites (liste vide, doublons, données corrompues).",
        "Prévoir un mode d'emploi court (commentaires d'en-tête).",
    ],
    "expert": [
        "Performance : justifier la complexité choisie.",
        "Robustesse : journalisation des erreurs et comportement déterministe.",
        "Livrable réutilisable : fonctions documentées, séparées de l'exécution.",
    ],
}

CRITERES_DE_BASE = [
    "Le programme s'exécute sans erreur sur les données d'exemple.",
    "Le résultat attendu est produit au format demandé.",
    "Les cas limites décrits dans l'énoncé sont traités.",
]


def contraintes(palier: int) -> str:
    tier = difficulte(palier)
    pool = CONTRAINTES[tier]
    return " ".join(f"- {c}" for c in pool)


def criteres(*extra: str) -> str:
    lignes = list(CRITERES_DE_BASE) + list(extra)
    return "\n".join(lignes)


def slug_unique(prefix: str, idx: int, texte: str, max_len: int = 150) -> str:
    """Slug déterministe, court et globalment unique (préfixe domaine + index)."""
    from django.utils.text import slugify
    base = slugify(texte)[:60]
    return f"{prefix}-{idx:05d}-{base}"
