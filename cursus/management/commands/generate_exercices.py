"""Génère le catalogue d'exercices (~10 000) par domaines.

Idempotent : les slugs générés sont déterministes (préfixe + index) et
`bulk_create(ignore_conflicts=True)` saute les lignes déjà présentes.

Usage :
    python manage.py generate_exercices
    python manage.py generate_exercices --python 6000 --reseaux 1800 --cyber 1400 \
        --vision 500 --iot 300 --graine 42
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from cursus.generators import GENERATEURS
from cursus.models import Domaine, Mission

# titre domaine -> (icone, couleur, sous_titre, défaut volume, ordre)
DOMAINES = {
    "Python": ("code-2", "bleu", "Algorithmique et données en Python pur", 6000, 1),
    "Réseaux informatiques": ("network", "vert", "Commutation, routage, services — Packet Tracer & Wireshark", 1800, 2),
    "Cybersécurité": ("shield", "rouge", "Laboratoire autorisé : attaquer pour apprendre à défendre", 1400, 3),
    "Vision par ordinateur": ("camera", "orange", "OpenCV : de l'image au système de vision", 500, 4),
    "Internet des objets": ("cpu", "violet", "ESP32/MicroPython simulés, capteurs, MQTT", 300, 5),
}


class Command(BaseCommand):
    help = "Génère les exercices du catalogue pour chaque domaine."

    def add_arguments(self, parser):
        parser.add_argument("--python", type=int, default=None, help="Volume Python pur.")
        parser.add_argument("--reseaux", type=int, default=None, help="Volume Réseaux.")
        parser.add_argument("--cyber", type=int, default=None, help="Volume Cybersécurité.")
        parser.add_argument("--vision", type=int, default=None, help="Volume Vision par ordinateur.")
        parser.add_argument("--iot", type=int, default=None, help="Volume Internet des objets.")
        parser.add_argument("--graine", type=int, default=42, help="Graine RNG (déterminisme).")

    def handle(self, *args, **opts):
        volumes = {
            "Python": opts["python"],
            "Réseaux informatiques": opts["reseaux"],
            "Cybersécurité": opts["cyber"],
            "Vision par ordinateur": opts["vision"],
            "Internet des objets": opts["iot"],
        }
        total_crees = 0
        for titre, (icone, couleur, sous_titre, defaut, ordre) in DOMAINES.items():
            domaine, created = Domaine.objects.get_or_create(
                titre=titre,
                defaults={"icone": icone, "couleur": couleur, "sous_titre": sous_titre,
                          "description": sous_titre, "ordre": ordre},
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Domaine créé : {titre}"))
            n = volumes[titre] if volumes[titre] is not None else defaut
            if n <= 0:
                continue
            gen = GENERATEURS[titre]
            rows = gen.generer(n, graine=opts["graine"])
            missions = []
            for row in rows:
                row.pop("numero", None)
                missions.append(Mission(domaine=domaine, **row))
            avant = Mission.objects.count()
            with transaction.atomic():
                Mission.objects.bulk_create(missions, batch_size=500, ignore_conflicts=True)
            gained = Mission.objects.count() - avant
            total_crees += gained
            self.stdout.write(
                f"{titre :24s} visé {n:6d} | nouveau {gained:6d} | en base "
                f"{Mission.objects.filter(domaine=domaine).count():6d}"
            )
        self.stdout.write(self.style.SUCCESS(
            f"Terminé. {total_crees} exercice(s) ajouté(s) — total catalogue : {Mission.objects.count()}"
        ))
