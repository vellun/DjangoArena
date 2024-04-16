from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, JsonResponse
import django.shortcuts
import django.views

import notifications.models


class NotificationsRecipientList(
    LoginRequiredMixin,
    UserPassesTestMixin,
    django.views.View,
):
    def get(self, *args, **kwargs):
        user_id = kwargs.get("user_id")
        cur_notifications = notifications.models.Notification.objects.filter(
            recipient=user_id,
        )
        return JsonResponse({"notifications": cur_notifications})


class NotificationsSenderList(
    LoginRequiredMixin,
    UserPassesTestMixin,
    django.views.View,
):
    def get(self, *args, **kwargs):
        user_id = kwargs.get("user_id")
        cur_notifications = notifications.models.Notification.objects.filter(
            sender=user_id,
        )
        return JsonResponse({"notifications": cur_notifications})


class DeleteNotification(django.views.View):
    model = notifications.models.Notification

    def get(self, *args, **kwargs):
        notification_id = kwargs.get("pk")
        notification = notifications.models.Notification.objects.get(
            pk=notification_id,
        )
        notification.delete()
        return HttpResponse("", status=200)


__all__ = []
