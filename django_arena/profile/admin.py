import core.models
import django.contrib
from django.contrib.admin import TabularInline
from django.contrib.auth.admin import User, UserAdmin
from profile.models import Problem
from sorl.thumbnail.admin import AdminImageMixin


class ProblemInline(AdminImageMixin, TabularInline):
    model = Problem
    can_delete = False
    fields = [
        Problem.title.field.name,
    ]


class CustomUser(UserAdmin):
    fields = (
        core.models.User.username.field.name,
        core.models.User.password.field.name,
        core.models.User.email.field.name,
        core.models.User.first_name.field.name,
        core.models.User.last_name.field.name,
    )

    inlines = (
        ProblemInline,
    )


django.contrib.admin.site.unregister(User)
django.contrib.admin.site.register(User, CustomUser)

__all__ = []
