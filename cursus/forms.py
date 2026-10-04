from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Profil


class BaseInputMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = "champ"
            if isinstance(field.widget, forms.CheckboxInput):
                css = "champ-check"
            field.widget.attrs.setdefault("class", css)
            field.widget.attrs.setdefault("placeholder", field.label or "")


class InscriptionForm(BaseInputMixin, UserCreationForm):
    email = forms.EmailField(required=True, label="Adresse e-mail")

    class Meta:
        model = User
        fields = ("username", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ConnexionForm(BaseInputMixin, AuthenticationForm):
    pass


class ProfilForm(BaseInputMixin, forms.ModelForm):
    class Meta:
        model = Profil
        fields = ("poste", "bio", "couleur_avatar")


class CompteForm(BaseInputMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
