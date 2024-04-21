import django.conf
import django.conf.urls.static
import django.contrib.admin
import django.contrib.auth.urls
import django.urls

import notifications.views


urlpatterns = [
    django.urls.path(
        "list/recipient/",
        notifications.views.NotificationsRecipientList.as_view(),
        name="notifications_recipient",
    ),
    django.urls.path(
        "list/sender",
        notifications.views.NotificationsSenderList.as_view(),
        name="notifications_sender",
    ),
    django.urls.path(
        "delete/<int:pk>/",
        notifications.views.DeleteNotification.as_view(),
        name="notification_delete",
    ),
]


__all__ = []
