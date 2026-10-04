from django.contrib import admin
from .models import (
    Domaine, Competence, Notion, Mission, Etape, Indice, CritereValidation,
    MissionProgress, EtapeValidation, Profil,
)


class NotionInline(admin.TabularInline):
    model = Notion
    extra = 0


class EtapeInline(admin.StackedInline):
    model = Etape
    extra = 0
    ordering = ["ordre"]


class IndiceInline(admin.StackedInline):
    model = Indice
    extra = 0
    ordering = ["ordre"]


class CritereInline(admin.TabularInline):
    model = CritereValidation
    extra = 0
    ordering = ["ordre"]


@admin.register(Domaine)
class DomaineAdmin(admin.ModelAdmin):
    list_display = ("titre", "icone", "couleur", "ordre", "publie")
    list_editable = ("ordre", "publie")
    prepopulated_fields = {"slug": ("titre",)}


@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    list_display = ("titre", "domaine", "niveau", "ordre", "publiee")
    list_filter = ("domaine", "niveau", "publiee")
    list_editable = ("ordre", "publiee")
    prepopulated_fields = {"slug": ("titre",)}
    inlines = [NotionInline]


@admin.register(Notion)
class NotionAdmin(admin.ModelAdmin):
    list_display = ("titre", "competence", "ordre")
    list_filter = ("competence__domaine", "competence")


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ("titre", "domaine", "palier", "type", "outils", "duree", "publiee")
    list_filter = ("domaine", "palier", "type", "publiee")
    search_fields = ("titre", "accroche", "contexte", "objectif")
    prepopulated_fields = {"slug": ("titre",)}
    filter_horizontal = ("competences_mobilisees",)
    inlines = [EtapeInline, IndiceInline, CritereInline]
    fieldsets = (
        ("Identification", {
            "fields": ("domaine", "palier", "titre", "slug", "type", "themes", "ordre", "publiee"),
        }),
        ("Carte (aperçu)", {
            "fields": ("accroche", "duree", "langage", "outils", "difficulte"),
        }),
        ("Mise en situation", {
            "fields": ("contexte", "probleme", "objectif", "environnement", "contraintes", "amorce"),
        }),
        ("Apprentissage & réussite", {
            "fields": ("ce_que_tu_apprends", "criteres_texte"),
        }),
        ("Rattachement historique (optionnel)", {
            "classes": ("collapse",),
            "fields": ("competence", "numero", "competences_mobilisees"),
        }),
    )


@admin.register(MissionProgress)
class MissionProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "mission", "terminee", "completed_at")
    list_filter = ("terminee", "mission__domaine")
    search_fields = ("user__username", "mission__titre")


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ("user", "poste", "streak_jours", "derniere_activite")
    search_fields = ("user__username",)
