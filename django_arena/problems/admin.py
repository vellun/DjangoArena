import django.contrib

import problems.models

django.contrib.admin.site.register(problems.models.Problem)


__all__ = []
