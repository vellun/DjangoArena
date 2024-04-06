import django.contrib

import core.models


django.contrib.admin.site.register(core.models.User)


__all__ = []
