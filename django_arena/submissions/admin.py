import django.contrib

import submissions.models


django.contrib.admin.site.register(submissions.models.Submission)


__all__ = []
