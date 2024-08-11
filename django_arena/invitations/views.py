import django.contrib
import django.shortcuts
import django.views

import core.models
import invitations.forms
import invitations.models


class SendInvite(django.views.View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = {
                "title": "Пригласить в группу",
                "form": invitations.forms.InviteFriendForm(),
            }
            return django.shortcuts.render(
                self.request,
                "invitations/add_friend.html",
                context,
            )

        django.contrib.messages.info(self.request, "Вы не аутентифицированы")
        return django.shortcuts.redirect(
            django.shortcuts.reverse("homepage:main"),
        )

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            form = invitations.forms.InviteFriendForm(self.request.POST)
            if form.is_valid():
                try:
                    user = core.models.User.objects.get(
                        username=self.request.POST.get("name"),
                    )
                except django.core.exceptions.ObjectDoesNotExist:
                    django.contrib.messages.error(
                        self.request,
                        "Такого пользователя не существует",
                    )
                    return django.shortcuts.redirect(
                        django.shortcuts.reverse("invitations:add_friend"),
                    )

                try:
                    invitations.InviteModel.objects.get(
                        user_from=self.request.user.id,
                        user_to=user.id,
                    )
                except django.core.exceptions.ObjectDoesNotExist:
                    pass
                else:
                    django.contrib.messages.error(
                        self.request,
                        "Приглашение уже отправлено",
                    )
                    return django.shortcuts.redirect(
                        django.shortcuts.reverse("invitations:add_friend"),
                    )

                try:
                    core.models.User.objects.get(
                        friends=user.id,
                        id=self.request.user.id,
                    )
                except django.core.exceptions.ObjectDoesNotExist:
                    pass
                else:
                    django.contrib.messages.error(
                        self.request,
                        "Вы уже в друзьях с пользователем",
                    )
                    return django.shortcuts.redirect(
                        django.shortcuts.reverse("invitations:add_friend"),
                    )

                if self.request.user.username == self.request.POST.get("name"):
                    django.contrib.messages.error(
                        self.request,
                        "Вы не можете отправить приглешние самому себе",
                    )
                    return django.shortcuts.redirect(
                        django.shortcuts.reverse("invitations:add_friend"),
                    )

                invitations.models.InviteModel.objects.create(
                    user_from=self.request.user,
                    user_to=user,
                    text=self.request.POST.get("text"),
                )
                django.contrib.messages.success(
                    self.request,
                    "Приглашение отправлено",
                )
                return django.shortcuts.redirect(
                    django.shortcuts.reverse("invitations:add_friend"),
                )

        django.contrib.messages.info(self.request, "Вы не аутентифицированы")
        return django.shortcuts.redirect(
            django.shortcuts.reverse("homepage:main"),
        )


class Invites(django.views.View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = {
                "title": "Приглашения",
                "invations": invitations.models.InviteModel.objects.filter(
                    user_to=self.request.user.id,
                ),
            }
            return django.shortcuts.render(
                self.request,
                "invitations/invite_list.html",
                context,
            )

        django.contrib.messages.info(self.request, "Вы не аутентифицированы")
        return django.shortcuts.redirect(
            django.shortcuts.reverse("homepage:main"),
        )


class InviteCard(django.views.View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = {
                "title": "Приглашения",
                "invite": invitations.models.InviteModel.objects.get(
                    user_to=self.request.user.id,
                    user_from=kwargs.get("pk"),
                ),
                "form": invitations.forms.AcceptOrReject(),
            }
            return django.shortcuts.render(
                self.request,
                "invitations/invite_card.html",
                context,
            )

        django.contrib.messages.info(self.request, "Вы не аутентифицированы")
        return django.shortcuts.redirect(
            django.shortcuts.reverse("homepage:main"),
        )

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            form = invitations.forms.AcceptOrReject(self.request.POST)
            if form.is_valid():
                if self.request.POST.get("is_accept"):
                    core.models.User.objects.get(
                        id=self.request.user.id,
                    ).friends.add(kwargs.get("pk"))
                    core.models.User.objects.get(
                        id=kwargs.get("pk"),
                    ).friends.add(self.request.user.id)
                    django.contrib.messages.success(
                        self.request,
                        "Вы были успешно добавлены в друзья",
                    )

                invitations.models.InviteModel.objects.get(
                    user_from=kwargs.get("pk"),
                    user_to=self.request.user.id,
                ).delete()
                return django.shortcuts.redirect(
                    django.shortcuts.reverse("invitations:invite_list"),
                )

            django.contrib.messages.error(self.request, "Форма не валидна")
            return django.shortcuts.redirect(
                django.shortcuts.reverse(
                    "invitations:invite_card",
                    args=[kwargs.get("pk")],
                ),
            )

        django.contrib.messages.info(self.request, "Вы не аутентифицированы")
        return django.shortcuts.redirect(
            django.shortcuts.reverse("homepage:main"),
        )


__all__ = [SendInvite, Invites, InviteCard]
