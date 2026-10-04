from django.apps import AppConfig


class CursusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cursus'
    verbose_name = 'Cursus & Missions'

    def ready(self):
        import cursus.signals  # noqa: F401
