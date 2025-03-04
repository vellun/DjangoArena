import django.views.generic.detail

import chatrooms.models


class GroupChatView(django.views.generic.detail.DetailView):
    model = chatrooms.models.ChatRoom
    template_name = "chat/group-chat.html"
    context_object_name = "chat"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        room = chatrooms.models.ChatRoom.objects.get(pk=pk)
        messages = chatrooms.models.Message.objects.select_related(
            "user",
        ).filter(room=room)
        context["messages"] = messages
        return context


__all__ = [GroupChatView]
