import json

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def to_json(value):
    """Sérialise un objet Python en JSON sûr pour injection JS."""
    return mark_safe(json.dumps(value, ensure_ascii=False))


@register.filter
def add1(value):
    return value + 1


@register.filter
def lignes(value):
    """Découpe un texte en lignes non vides (pour les outils/labels)."""
    if not value:
        return []
    return [ln.strip("-•* ") for ln in str(value).splitlines() if ln.strip()]


@register.filter
def liste_csv(value):
    """Découpe une chaîne CSV en éléments propres (thèmes, outils...)."""
    if not value:
        return []
    return [p.strip() for p in str(value).split(",") if p.strip()]
