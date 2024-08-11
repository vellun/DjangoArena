import django.contrib.admin

import chatrooms.models


django.contrib.admin.site.register(chatrooms.models.ChatRoom)
django.contrib.admin.site.register(chatrooms.models.Message)


__all__ = []
