import core.models
import notifications.models


def get_notifications(request):
    if request.user.is_authenticated:
        user = core.models.User.objects.get(pk=request.user.id)
        cur_notifications = notifications.models.Notification.objects.filter(
            recipient=user.id,
        )
    else:
        cur_notifications = []

    return {"notifications": cur_notifications}


__all__ = ["get_notifications"]
