"""Flux unique : catalogue d'exercices -> fiche -> résolu -> suivant.

Pas de parcours, pas de compétences côté utilisateur : filtrer, lire la
mise en situation, coder chez soi, cliquer « Je l'ai résolu ».
"""

from collections import Counter
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from . import services
from .forms import CompteForm, InscriptionForm, ConnexionForm, ProfilForm
from .models import Domaine, Mission, Indice, IndiceVue, MissionProgress


def _url(base, params, **kw):
    """Construit une URL de filtre en préservant les autres paramètres GET.

    Une valeur vide ("" ou None) retire le paramètre de l'URL (déclenche un filtre).
    """
    merged = {k: v for k, v in params.items() if v and k != "page"}
    for k, v in kw.items():
        if v:
            merged[k] = v
        else:
            merged.pop(k, None)
    return base + ("?" + urlencode(merged) if merged else "")


# ---------------------------------------------------------------------------
# Accueil public
# ---------------------------------------------------------------------------

def accueil(request):
    if request.user.is_authenticated:
        return redirect("catalogue")
    domaines = Domaine.objects.filter(publie=True)
    stats = {
        "domaines": domaines.count(),
        "exercices": Mission.objects.filter(publiee=True).count(),
    }
    return render(request, "cursus/accueil.html", {
        "domains": domaines, "stats": stats,
        "steps": ["Contexte", "Tâche", "Indices", "VSCode", "Résolu"],
        "outils": [
            {"nom": "Python", "icon": "python"},
            {"nom": "VSCode", "icon": "vscode"},
            {"nom": "Cisco Packet Tracer", "icon": "cisco"},
            {"nom": "Wireshark", "icon": "wireshark"},
            {"nom": "Nmap", "icon": "nmap"},
            {"nom": "Kali Linux", "icon": "kali"},
            {"nom": "OpenCV", "icon": "opencv"},
            {"nom": "Tinkercad Circuits", "icon": "tinkercad"},
            {"nom": "Mosquitto (MQTT)", "icon": "mosquitto"},
            {"nom": "MicroPython", "icon": "micropython"},
        ],
    })


# ---------------------------------------------------------------------------
# Authentification
# ---------------------------------------------------------------------------

def inscription(request):
    if request.user.is_authenticated:
        return redirect("catalogue")
    form = InscriptionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Bienvenue sur Praxis ! Votre catalogue vous attend.")
        return redirect("catalogue")
    return render(request, "cursus/inscription.html", {"form": form})


def connexion(request):
    if request.user.is_authenticated:
        return redirect("catalogue")
    form = ConnexionForm(request, request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect("catalogue")
    return render(request, "cursus/connexion.html", {"form": form})


def deconnexion(request):
    logout(request)
    return redirect("accueil")


# ---------------------------------------------------------------------------
# Catalogue d'exercices ( écran principal )
# ---------------------------------------------------------------------------

TYPES = [("exercice", "Exercice"), ("projet", "Projet"), ("laboratoire", "Laboratoire"), ("pentest", "Pentest")]


@login_required
def catalogue(request):
    params = {k: request.GET.get(k, "").strip() for k in ("domaine", "palier", "type", "theme", "q", "etat")}

    qs = (
        Mission.objects.filter(publiee=True)
        .select_related("domaine")
        .defer("contexte", "probleme", "objectif", "environnement",
               "contraintes", "amorce", "ce_que_tu_apprends", "criteres_texte")
    )
    if params["domaine"]:
        qs = qs.filter(domaine__slug=params["domaine"])
    if params["palier"].isdigit():
        qs = qs.filter(palier=int(params["palier"]))
    if params["type"] in dict(TYPES):
        qs = qs.filter(type=params["type"])
    if params["theme"]:
        qs = qs.filter(themes__icontains=params["theme"])
    if params["q"]:
        qs = qs.filter(Q(titre__icontains=params["q"]) | Q(accroche__icontains=params["q"]))

    finis = services.done_ids(request.user)
    if params["etat"] == "fait":
        qs = qs.filter(pk__in=finis)
    elif params["etat"] == "non":
        qs = qs.exclude(pk__in=finis)

    paginator = Paginator(qs, 48)
    page_obj = paginator.get_page(request.GET.get("page") or 1)
    for m in page_obj:
        m.faite = m.pk in finis

    # Lien de pagination : conserve les filtres actifs.
    page_qs = urlencode({k: v for k, v in params.items() if v})
    cur = page_obj.number
    total_pages = paginator.num_pages
    window = [p for p in range(max(1, cur - 3), min(total_pages, cur + 3) + 1)]

    # Chips de filtres (avec compteurs quand c'est léger).
    base = request.path
    domaines = (
        Domaine.objects.filter(publie=True)
        .annotate(nb=Count("exercices", filter=Q(exercices__publiee=True)))
        .order_by("ordre", "titre")
    )
    for d in domaines:
        d.chip_url = _url(base, params, domaine=d.slug)
        d.actif = params["domaine"] == d.slug

    paliers = []
    for p in range(1, 11):
        paliers.append({
            "n": p, "actif": params["palier"] == str(p),
            "url": _url(base, params, palier=str(p) if params["palier"] != str(p) else ""),
        })

    types = [{"code": c, "nom": n, "actif": params["type"] == c,
              "url": _url(base, params, type=c if params["type"] != c else "")} for c, n in TYPES]

    theme_counts = Counter(
        t.strip()
        for t in Mission.objects.filter(publiee=True).exclude(themes="")
                                 .values_list("themes", flat=True)
        for t in t.split(",") if t.strip()
    )
    themes = [{"nom": nom, "actif": params["theme"] == nom,
               "url": _url(base, params, theme=nom if params["theme"] != nom else "")}
              for nom, _ in theme_counts.most_common(10)]

    etats = [
        {"code": "non", "nom": "Non résolus", "actif": params["etat"] == "non",
         "url": _url(base, params, etat="non" if params["etat"] != "non" else "")},
        {"code": "fait", "nom": "Résolus", "actif": params["etat"] == "fait",
         "url": _url(base, params, etat="fait" if params["etat"] != "fait" else "")},
    ]

    return render(request, "cursus/catalogue.html", {
        "page_obj": page_obj,
        "total": paginator.count,
        "params": params,
        "page_qs": page_qs,
        "page_window": window,
        "total_pages": total_pages,
        "chips_domaines": domaines,
        "chips_paliers": paliers,
        "chips_types": types,
        "chips_themes": themes,
        "chips_etats": etats,
        "effacer_url": base,
        "nb_resolus": len(finis),
        # Options « Tous » des sélecteurs : retirent leur paramètre sans toucher aux autres.
        "domaine_tous_url": _url(base, {**params, "domaine": ""}),
        "type_tous_url": _url(base, {**params, "type": ""}),
        "theme_tous_url": _url(base, {**params, "theme": ""}),
        "etat_tous_url": _url(base, {**params, "etat": ""}),
    })


# ---------------------------------------------------------------------------
# Fiche exercice
# ---------------------------------------------------------------------------

def _contexte_mission(user, mission):
    etapes = list(mission.etapes.all())
    mp = MissionProgress.objects.filter(user=user, mission=mission).first()
    indices = list(mission.indices.all())
    vus = set(
        IndiceVue.objects.filter(user=user, indice__mission=mission).values_list("indice_id", flat=True)
    )
    prochain_indice = next((i for i in indices if i.pk not in vus), None)
    return {
        "mission": mission,
        "etapes": etapes,
        "indices": indices,
        "indices_vus": vus,
        "prochain_indice": prochain_indice,
        "criteres": mission.criteres.all(),
        "progress": mp,
        "terminee": bool(mp and mp.terminee),
    }


@login_required
def mission_detail(request, slug):
    mission = get_object_or_404(
        Mission.objects.select_related("domaine"), slug=slug, publiee=True,
    )
    ctx = _contexte_mission(request.user, mission)
    ctx["suivante"] = services.prochaine_mission(request.user, apres=mission)
    return render(request, "cursus/mission_detail.html", ctx)


@login_required
def afficher_indice(request, indice_id):
    indice = get_object_or_404(Indice, pk=indice_id)
    IndiceVue.objects.get_or_create(user=request.user, indice=indice)
    if request.headers.get("HX-Request"):
        ctx = _contexte_mission(request.user, indice.mission)
        return render(request, "cursus/partials/_indices.html", ctx)
    return redirect("mission_detail", slug=indice.mission.slug)


@login_required
@transaction.atomic
def terminer_mission(request, slug):
    if request.method != "POST":
        return HttpResponseForbidden()
    mission = get_object_or_404(Mission.objects.select_related("domaine"), slug=slug, publiee=True)
    # L'utilisateur a codé chez lui (VSCode) : il déclare l'exercice résolu ici.
    mp, _ = MissionProgress.objects.get_or_create(user=request.user, mission=mission)
    if not mp.terminee:
        mp.mark_completed()
    services.maj_streak(request.user)
    messages.success(request, f"Résolu : « {mission.titre} ».")
    if request.POST.get("suite") == "rester":
        return redirect("mission_detail", slug=slug)
    suivante = services.prochaine_mission(request.user, apres=mission)
    if suivante:
        return redirect("mission_detail", slug=suivante.slug)
    return redirect("progression")


@login_required
def rouvrir_mission(request, slug):
    if request.method != "POST":
        return HttpResponseForbidden()
    mission = get_object_or_404(Mission, slug=slug, publiee=True)
    MissionProgress.objects.filter(user=request.user, mission=mission).update(
        terminee=False, completed_at=None
    )
    messages.info(request, "Exercice rouvert (non résolu).")
    return redirect("mission_detail", slug=slug)


# ---------------------------------------------------------------------------
# Progression & compte
# ---------------------------------------------------------------------------

@login_required
def mission_prochaine(request):
    suivante = services.prochaine_mission(request.user)
    if not suivante:
        messages.success(request, "Tous les exercices disponibles sont résolus.")
        return redirect("progression")
    return redirect("mission_detail", slug=suivante.slug)


@login_required
def progression(request):
    return render(request, "cursus/progression.html", services.progression_donnees(request.user))


@login_required
def profil(request):
    user = request.user
    return render(request, "cursus/profil.html", {
        "stats": services.progression_donnees(user),
    })


@login_required
def parametres(request):
    user = request.user
    compte_form = CompteForm(request.POST or None, instance=user, prefix="compte")
    profil_form = ProfilForm(request.POST or None, instance=user.profil, prefix="profil")

    if request.method == "POST":
        if "enregistrer_compte" in request.POST and compte_form.is_valid():
            compte_form.save()
            messages.success(request, "Compte mis à jour.")
            return redirect("parametres")
        if "enregistrer_profil" in request.POST and profil_form.is_valid():
            profil_form.save()
            messages.success(request, "Profil mis à jour.")
            return redirect("parametres")
    return render(request, "cursus/parametres.html", {
        "compte_form": compte_form, "profil_form": profil_form,
    })
