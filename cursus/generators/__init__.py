"""Générateurs d'exercices par domaine (voir base.py pour le contrat)."""

from . import cyber_gen, iot_gen, python_gen, reseaux_gen, vision_gen

# clé = titre du Domaine en base
GENERATEURS = {
    "Python": python_gen,
    "Réseaux informatiques": reseaux_gen,
    "Cybersécurité": cyber_gen,
    "Vision par ordinateur": vision_gen,
    "Internet des objets": iot_gen,
}

__all__ = ["GENERATEURS", "python_gen", "reseaux_gen", "cyber_gen", "vision_gen", "iot_gen"]
