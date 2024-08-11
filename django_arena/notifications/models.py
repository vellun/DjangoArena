from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    class NotificationTypes(models.TextChoices):
        SYSTEM = "SN", _("System notification")
        GROUP = "GN", _("Group notification")
        FRIEND = "FN", _("Friend notification")
        UNKNOWN = "UN", _("Unknown notification")
        OTHER = "ON", _("Other notification")

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sended_emails",
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_emails",
    )
    notification_type = models.CharField(
        max_length=2,
        choices=NotificationTypes.choices,
        default=NotificationTypes.SYSTEM,
    )
    text = models.CharField(max_length=511, null=True, blank=True)

    class Meta:
        verbose_name = "уведомление"
        verbose_name_plural = "уведомления"

    def __str__(self):
        return (
            f"{self.notification_type} {str(self.sender)}"
            f" {str(self.recipient)} {str(self.text)}"
        )


__all__ = [Notification]
