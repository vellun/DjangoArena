from django.contrib import admin

import notifications.models


admin.site.register(notifications.models.Notification)
