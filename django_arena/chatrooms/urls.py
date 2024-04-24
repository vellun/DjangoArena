import django.urls

import chatrooms.views

app_name = "chat"

urlpatterns = [
    django.urls.path(
        "<int:pk>/",
        chatrooms.views.GroupChatView.as_view(),
        name="group-chat",
    ),
]
