from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone


class SlugableModel(models.Model):
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.slug_source) or "element"
            slug = base
            n = 1
            model_cls = self.__class__
            while model_cls.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f"{base}-{n}"
            self.slug = slug
        super().save(*args, **kwargs)


class Domaine(SlugableModel):
    """Un domaine informatique : Python, Réseaux, Cybersécurité..."""

    COULEURS = [
        ("bleu", "Bleu"),
        ("vert", "Vert"),
        ("violet", "Violet"),
        ("orange", "Orange"),
        ("rouge", "Rouge"),
        ("sombre", "Sombre"),
    ]

    titre = models.CharField("Titre", max_length=120)
    sous_titre = models.CharField("Sous-titre", max_length=200, blank=True)
    description = models.TextField("Description courte", blank=True)
    icone = models.CharField("Icône (nom Lucide)", max_length=40, default="code-2")
    couleur = models.CharField("Couleur", max_length=12, choices=COULEURS, default="bleu")
    ordre = models.PositiveIntegerField("Ordre", default=0)
    publie = models.BooleanField("Publié", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Domaine"
        verbose_name_plural = "Domaines"
        ordering = ["ordre", "titre"]

    @property
    def slug_source(self):
        return self.titre

    def __str__(self):
        return self.titre


class Competence(SlugableModel):
    """Une compétence rattachée à un domaine."""

    NIVEAUX = [
        ("debutant", "Débutant"),
        ("intermediaire", "Intermédiaire"),
        ("avance", "Avancé"),
        ("expert", "Expert"),
    ]

    domaine = models.ForeignKey(Domaine, on_delete=models.CASCADE, related_name="competences")
    titre = models.CharField("Titre", max_length=140)
    description = models.TextField("Description courte", blank=True)
    niveau = models.CharField("Niveau visé", max_length=14, choices=NIVEAUX, default="debutant")
    ordre = models.PositiveIntegerField("Ordre", default=0)
    publiee = models.BooleanField("Publiée", default=True)

    class Meta:
        verbose_name = "Compétence"
        verbose_name_plural = "Compétences"
        ordering = ["domaine", "ordre", "titre"]

    @property
    def slug_source(self):
        return self.titre

    def __str__(self):
        return f"{self.titre} ({self.domaine.titre})"


class Notion(SlugableModel):
    """Une notion essentielle — volontairement concise."""

    competence = models.ForeignKey(Competence, on_delete=models.CASCADE, related_name="notions")
    titre = models.CharField("Titre", max_length=140)
    resume = models.TextField("L'essentiel en quelques lignes")
    ordre = models.PositiveIntegerField("Ordre", default=0)

    class Meta:
        verbose_name = "Notion"
        verbose_name_plural = "Notions"
        ordering = ["competence", "ordre"]

    @property
    def slug_source(self):
        return self.titre

    def __str__(self):
        return self.titre


class Mission(SlugableModel):
    """Un exercice : mise en situation professionnelle réelle. Cœur du catalogue."""

    TYPES = [
        ("exercice", "Exercice"),
        ("projet", "Projet"),
        ("laboratoire", "Laboratoire"),
        ("pentest", "Pentest"),
    ]

    DIFFICULTES = Competence.NIVEAUX

    domaine = models.ForeignKey(
        Domaine, on_delete=models.CASCADE, null=True, blank=True,
        related_name="exercices", verbose_name="Domaine",
    )
    # Relique du parcours : conservée mais facultative (le catalogue s'appuie sur `domaine`).
    competence = models.ForeignKey(
        Competence, on_delete=models.CASCADE, null=True, blank=True,
        related_name="missions", verbose_name="Compétence (optionnel)",
    )
    numero = models.PositiveIntegerField("Numéro", default=1)
    titre = models.CharField("Titre", max_length=180)
    accroche = models.CharField("Accroche (une phrase)", max_length=200, blank=True,
                               help_text="Une phrase courte qui donne envie. Affichée sur la carte.")
    duree = models.CharField("Durée estimée", max_length=20, blank=True, default="45 min")
    langage = models.CharField("Langage attendu", max_length=12, default="python",
                               choices=[("python", "Python"), ("bash", "Bash / Linux"),
                                        ("cisco", "CLI Cisco"), ("texte", "Texte / autre")])
    outils = models.CharField("Outils", max_length=200, blank=True, default="Python / VSCode",
                              help_text="Ex : Cisco Packet Tracer, Wireshark, Nmap…")
    palier = models.PositiveSmallIntegerField("Palier (1-10)", default=1,
                                              help_text="Niveau fin dans le domaine : 1 = plus facile, 10 = plus dur.")
    themes = models.CharField("Thèmes (séparés par virgules)", max_length=220, blank=True,
                              help_text="Ex : algo, data, fichiers, api, reseau, smb, securite, pentest…")
    type = models.CharField("Type", max_length=14, choices=TYPES, default="exercice")
    difficulte = models.CharField("Difficulté", max_length=14, choices=DIFFICULTES, default="debutant")

    contexte = models.TextField("Contexte")
    probleme = models.TextField("Problème")
    objectif = models.TextField("Objectif")
    environnement = models.TextField("Environnement (outils)", blank=True)
    contraintes = models.TextField("Contraintes", blank=True)
    amorce = models.TextField("Amorce de code (optionnel)", blank=True,
                              help_text="Point de départ que l'utilisateur peut copier dans son éditeur (VSCode).")
    ce_que_tu_apprends = models.TextField("Ce que tu apprends / maîtrises", blank=True)
    criteres_texte = models.TextField("Critères de réussite (une ligne par critère)", blank=True,
                                      help_text="Utilisé si aucun critère n'est saisi en ligne.")

    # Compétences réellement mobilisées (peuvent traverser plusieurs domaines)
    competences_mobilisees = models.ManyToManyField(
        Competence, blank=True, related_name="missions_transversales",
        verbose_name="Compétences mobilisées",
    )
    publiee = models.BooleanField("Publiée", default=True)
    ordre = models.PositiveIntegerField("Ordre", default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Exercice"
        verbose_name_plural = "Exercices"
        ordering = ["domaine", "palier", "ordre", "numero", "id"]

    @property
    def slug_source(self):
        return f"exo-{self.titre}"
    
    @property
    def niveau_label(self):
        """Libellé court du palier pour l'affichage."""
        return f"Palier {self.palier}/10"
    
    def __str__(self):
        return f"{self.titre} ({self.domaine or self.competence})"


class Etape(models.Model):
    """Une tâche à cocher dans 'VOTRE MISSION'."""

    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="etapes")
    texte = models.CharField("Énoncé de l'étape", max_length=300)
    ordre = models.PositiveIntegerField("Ordre", default=0)

    class Meta:
        verbose_name = "Étape"
        verbose_name_plural = "Étapes"
        ordering = ["ordre"]

    def __str__(self):
        return f"{self.mission} · Étape {self.ordre}"


class Indice(models.Model):
    """Un indice progressif."""

    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="indices")
    texte = models.TextField("Indice")
    ordre = models.PositiveIntegerField("Ordre", default=0)

    class Meta:
        verbose_name = "Indice"
        verbose_name_plural = "Indices"
        ordering = ["ordre"]

    def __str__(self):
        return f"Indice {self.ordre} · {self.mission}"


class CritereValidation(models.Model):
    """Un critère vérifié lors de la validation."""

    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="criteres")
    texte = models.CharField("Critère", max_length=300)
    ordre = models.PositiveIntegerField("Ordre", default=0)

    class Meta:
        verbose_name = "Critère de validation"
        verbose_name_plural = "Critères de validation"
        ordering = ["ordre"]

    def __str__(self):
        return f"{self.mission} · {self.texte[:30]}"


# ----------------------------------------------------------------------------
# Progression & validation (orientée compétences)
# ----------------------------------------------------------------------------


class MissionProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="progress_missions")
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="progress")
    terminee = models.BooleanField("Terminée", default=False)
    started_at = models.DateTimeField("Démarrée le", auto_now_add=True)
    completed_at = models.DateTimeField("Terminée le", null=True, blank=True)

    class Meta:
        verbose_name = "Progression mission"
        verbose_name_plural = "Progression des missions"
        unique_together = ("user", "mission")

    def mark_completed(self):
        if not self.terminee:
            self.terminee = True
            self.completed_at = timezone.now()
            self.save()


class EtapeValidation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="etapes_validees")
    etape = models.ForeignKey(Etape, on_delete=models.CASCADE, related_name="validations")
    done = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "etape")


class IndiceVue(models.Model):
    """Trace des indices consultés (aide progressive)."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="indices_vus")
    indice = models.ForeignKey(Indice, on_delete=models.CASCADE, related_name="vus")

    class Meta:
        unique_together = ("user", "indice")


class Profil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profil")
    poste = models.CharField("Poste / rôle", max_length=120, blank=True)
    bio = models.TextField("Présentation", blank=True)
    couleur_avatar = models.CharField("Couleur avatar", max_length=12, default="bleu")
    streak_jours = models.PositiveIntegerField("Série (jours)", default=0)
    derniere_activite = models.DateField("Dernière activité", null=True, blank=True)

    def __str__(self):
        return f"Profil de {self.user.username}"
