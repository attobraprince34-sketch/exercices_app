from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from cursus.models import (
    Domaine, Competence, Notion, Mission, Etape, Indice, CritereValidation,
    MissionProgress, EtapeValidation, Profil,
)
from cursus.demo_content import CONTENU

PALIER_PAR_DIFFICULTE = {"debutant": 2, "intermediaire": 5, "avance": 8, "expert": 10}


class Command(BaseCommand):
    help = "Charge le contenu de démonstration réaliste (Python, Réseaux, Cybersécurité)."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Réinitialise tout le contenu avant peuplement.")

    def handle(self, *args, **opts):
        if opts["reset"]:
            for model in (CritereValidation, Indice, Etape, Mission, Notion, Competence, Domaine):
                model.objects.all().delete()
            self.stdout.write(self.style.WARNING("Contenu réinitialisé."))

        total_missions = 0
        for bloc in CONTENU:
            d = bloc["domaine"]
            domaine, _ = Domaine.objects.get_or_create(
                titre=d["titre"],
                defaults={
                    "sous_titre": d.get("sous_titre", ""), "description": d.get("description", ""),
                    "icone": d.get("icone", "layers"), "couleur": d.get("couleur", "bleu"),
                    "ordre": d.get("ordre", 99),
                },
            )
            for comp in bloc["competences"]:
                competence, _ = Competence.objects.get_or_create(
                    domaine=domaine, titre=comp["titre"],
                    defaults={"description": comp.get("description", ""),
                              "niveau": comp.get("niveau", "debutant"), "ordre": comp.get("ordre", 0)},
                )
                for i, n in enumerate(comp.get("notions", [])):
                    Notion.objects.get_or_create(
                        competence=competence, titre=n["titre"],
                        defaults={"resume": n["resume"], "ordre": i},
                    )
                for i, m in enumerate(comp["missions"]):
                    mission, created = Mission.objects.get_or_create(
                        competence=competence, numero=m["numero"], titre=m["titre"],
                        defaults={
                            "domaine": domaine,
                            "palier": PALIER_PAR_DIFFICULTE.get(m["difficulte"], 1),
                            "type": m["type"], "difficulte": m["difficulte"],
                            "accroche": m.get("accroche", ""),
                            "duree": m.get("duree", "45 min"),
                            "langage": m.get("langage", "python"),
                            "amorce": m.get("amorce", ""),
                            "contexte": m["contexte"], "probleme": m["probleme"],
                            "objectif": m["objectif"], "environnement": m["environnement"],
                            "contraintes": m["contraintes"], "ordre": i,
                        },
                    )
                    total_missions += 1
                    if created:
                        for j, e in enumerate(m["etapes"]):
                            Etape.objects.create(mission=mission, texte=e, ordre=j + 1)
                        for j, ind in enumerate(m.get("indices", [])):
                            Indice.objects.create(mission=mission, texte=ind, ordre=j + 1)
                        for j, cr in enumerate(m.get("criteres", [])):
                            CritereValidation.objects.create(mission=mission, texte=cr, ordre=j + 1)

                    # Compétences mobilisées (résolues par titre)
                    mobilisees = set(m.get("mobilise", [])) | {competence.titre}
                    pks = list(Competence.objects.filter(titre__in=mobilisees).values_list("pk", flat=True))
                    mission.competences_mobilisees.set(pks)

        self._creer_utilisateurs()

        self.stdout.write(self.style.SUCCESS(
            f"OK — {Domaine.objects.count()} domaines, "
            f"{Competence.objects.count()} compétences, "
            f"{Mission.objects.count()} missions chargées."
        ))

    def _creer_utilisateurs(self):
        # Compte admin
        admin, is_new = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@praxis.local", "is_staff": True, "is_superuser": True},
        )
        if is_new:
            admin.set_password("praxis-admin-2026")
            admin.save()

        # Compte de démonstration avec un peu de progression
        demo, is_new = User.objects.get_or_create(
            username="demo",
            defaults={"email": "demo@praxis.local", "first_name": "Camille", "last_name": "Dupont"},
        )
        if is_new:
            demo.set_password("praxis-demo-2026")
            demo.save()
            self._simuler_progression(demo)

    def _simuler_progression(self, user):
        """Valide quelques missions pour un tableau de bord de démonstration vivant."""
        Profil.objects.update_or_create(
            user=user, defaults={"poste": "Technicien support en reconversion", "couleur_avatar": "violet"},
        )
        titres_a_terminer = [
            "Vérifier la conformité des mots de passe internes",
            "Automatiser la gestion des utilisateurs d'une entreprise",
            "Mettre en place le réseau local d'une nouvelle agence",
            "Durcir l'accès SSH d'un serveur",
        ]
        for titre in titres_a_terminer:
            mission = Mission.objects.filter(titre=titre).first()
            if not mission:
                continue
            mp, _ = MissionProgress.objects.get_or_create(user=user, mission=mission)
            for etape in mission.etapes.all():
                EtapeValidation.objects.update_or_create(user=user, etape=etape, defaults={"done": True})
            mp.mark_completed()
        user.profil.streak_jours = 4
        user.profil.derniere_activite = timezone.now().date()
        user.profil.save()
