from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("", views.accueil, name="accueil"),

    # Authentification
    path("inscription/", views.inscription, name="inscription"),
    path("connexion/", views.connexion, name="connexion"),
    path("deconnexion/", views.deconnexion, name="deconnexion"),

    # Catalogue = écran de travail unique
    path("exercices/", views.catalogue, name="catalogue"),
    path("tableau-de-bord/", RedirectView.as_view(pattern_name="catalogue", permanent=False)),
    path("parcours/", RedirectView.as_view(pattern_name="catalogue", permanent=False)),

    # Fiche exercice
    path("mission/<slug:slug>/", views.mission_detail, name="mission_detail"),
    path("continuer/", views.mission_prochaine, name="mission_prochaine"),
    path("mission/<slug:slug>/terminer/", views.terminer_mission, name="terminer_mission"),
    path("mission/<slug:slug>/rouvrir/", views.rouvrir_mission, name="rouvrir_mission"),
    path("indice/<int:indice_id>/voir/", views.afficher_indice, name="afficher_indice"),

    # Progression minimale + compte
    path("progression/", views.progression, name="progression"),
    path("profil/", views.profil, name="profil"),
    path("parametres/", views.parametres, name="parametres"),
]
