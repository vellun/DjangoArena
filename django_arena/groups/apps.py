from django.apps import AppConfig


class GroupsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "groups"
    verbose_name = "Группы"

    def ready(self):
        import groups.signals


__all__ = []
