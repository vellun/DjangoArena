import django.contrib.admin

import chatrooms.models


django.contrib.admin.site.register(chatrooms.models.ChatRoom)


__all__ = []
