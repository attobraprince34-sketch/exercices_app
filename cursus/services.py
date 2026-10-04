"""Logique minimale du catalogue d'exercices : résolu / suivant / progression."""

from datetime import timedelta

from django.db.models import Count
from django.utils import timezone

from .models import Domaine, Mission, MissionProgress, Profil


def done_ids(user):
    """IDs des exercices marqués résolus par l'utilisateur."""
    if not user.is_authenticated:
        return set()
    return set(
        MissionProgress.objects.filter(user=user, terminee=True).values_list("mission_id", flat=True)
    )


def prochaine_mission(user, apres=None):
    """Premier exercice non résolu, dans l'ordre du catalogue (domaine, palier).

    Si `apres` est fourni, cherche le suivant non résolu après celui-ci dans
    l'ordre ; sinon retombe sur le premier non résolu global.
    """
    finies = done_ids(user)
    qs = Mission.objects.filter(publiee=True).exclude(pk__in=finies).select_related("domaine")
    if apres is not None:
        suivant = (
            qs.filter(domaine=apres.domaine, palier__gte=apres.palier)
            .exclude(pk=apres.pk).order_by("palier", "ordre", "id").first()
        )
        if suivant:
            return suivant
    return qs.first()


def progression_donnees(user):
    """Vue minimale : totals, barres par domaine et par palier, série, récents."""
    finies = MissionProgress.objects.filter(user=user, terminee=True)
    total_faites = finies.count()
    total_exercices = Mission.objects.filter(publiee=True).count()

    faites_ids = list(finies.values_list("mission_id", flat=True))

    par_domaine = []
    for d in Domaine.objects.filter(publie=True):
        nb_total = Mission.objects.filter(domaine=d, publiee=True).count()
        nb_faites = Mission.objects.filter(domaine=d, publiee=True, pk__in=faites_ids).count()
        par_domaine.append({
            "domaine": d, "faites": nb_faites, "total": nb_total,
            "pct": round(nb_faites * 100 / nb_total) if nb_total else 0,
        })

    faits_par_palier = dict(
        Mission.objects.filter(pk__in=faites_ids).values_list("palier").annotate(n=Count("id"))
    )
    par_palier = [{"palier": p, "nb": faits_par_palier.get(p, 0)} for p in range(1, 11)]

    derniers = (
        finies.select_related("mission", "mission__domaine")
        .order_by("-completed_at")[:8]
    )

    profil = getattr(user, "profil", None)
    return {
        "total_faites": total_faites,
        "total_exercices": total_exercices,
        "pct_global": round(total_faites * 100 / total_exercices) if total_exercices else 0,
        "par_domaine": par_domaine,
        "par_palier": par_palier,
        "max_palier_faite": max(
            (m.mission.palier for m in derniers if m.mission.palier), default=0
        ),
        "streak": profil.streak_jours if profil else 0,
        "derniers": derniers,
    }


def maj_streak(user):
    profil = getattr(user, "profil", None) or Profil.objects.create(user=user)
    aujourdhui = timezone.now().date()
    if profil.derniere_activite == aujourdhui:
        return profil
    if profil.derniere_activite and (aujourdhui - profil.derniere_activite) <= timedelta(days=1):
        profil.streak_jours += 1
    else:
        profil.streak_jours = 1
    profil.derniere_activite = aujourdhui
    profil.save()
    return profil
