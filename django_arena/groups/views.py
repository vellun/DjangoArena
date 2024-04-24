import django.contrib.messages
import django.core.exceptions
import django.db.models
import django.shortcuts
import django.urls
import django.views

import core.models
import groups.forms
import groups.models


class GroupPage(django.views.View):
    def get(self, *args, **kwargs):
        group = django.shortcuts.get_object_or_404(
            groups.models.Group,
            pk=kwargs.get("pk"),
        )
        try:
            group_user = groups.models.GroupUser.objects.get(
                user_id=self.request.user.id,
                group_id=kwargs.get("pk"),
            )
        except groups.models.GroupUser.DoesNotExist:
            group_user = None

        if self.request.user.is_authenticated:
            context = {
                "title": "Группа",
                "item": kwargs.get("pk"),
                "group": group,
                "delete": groups.forms.DeleteForm(),
                "user": group_user,
            }
            return django.shortcuts.render(
                self.request,
                "group/group.html",
                context,
            )

        django.contrib.messages.info(self.request, "Вы не аутентифицированы")
        return django.shortcuts.redirect(
            django.shortcuts.reverse("homepage:main"),
        )

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            form = groups.forms.DeleteForm(self.request.POST)
            if form.is_valid():
                if self.request.POST.get("is_delete") == "Удалить":
                    groups.models.Group.objects.get(
                        id=kwargs.get("pk"),
                    ).delete()
                    django.contrib.messages.info(
                        self.request,
                        "Группа успешно удалена",
                    )
                    return django.shortcuts.redirect(
                        django.shortcuts.reverse("homepage:main"),
                    )

            django.contrib.messages.info(self.request, "Форма не валидна")
            return django.shortcuts.redirect(
                django.shortcuts.reverse("homepage:main"),
            )

        django.contrib.messages.info(self.request, "Вы не аутентифицированы")
        return django.shortcuts.redirect(
            django.shortcuts.reverse("homepage:main"),
        )


class GroupMyView(django.views.View):
    def get(self, *args, **kwargs):
        user_groups = self.request.user.group_user.values_list(
            "group",
            flat=True,
        )
        selected_groups = groups.models.Group.objects.filter(
            id__in=user_groups,
        )

        context = {
            "title": "Группы",
            "tab": "my",
            "groups": selected_groups,
        }

        return django.shortcuts.render(
            request=self.request,
            template_name="group/user_group.html",
            context=context,
        )


class GroupAllView(django.views.View):
    def get(self, *args, **kwargs):
        selected_groups = groups.models.Group.objects.all().order_by(
            "-created_at",
        )
        context = {
            "title": "Искать группы",
            "tab": "all",
            "groups": selected_groups,
        }
        return django.shortcuts.render(
            request=self.request,
            template_name="group/user_group.html",
            context=context,
        )


class GroupCreate(django.views.View):
    def get(self, *args, **kwargs):
        form = groups.forms.GroupForm()
        context = {
            "title": "Создать группу",
            "form": form,
        }
        return django.shortcuts.render(
            self.request,
            "group/new_group.html",
            context,
        )

    def post(self, *args, **kwargs):
        form = groups.forms.GroupForm(self.request.POST)
        context = {
            "title": "Группа",
            "group_form": form,
        }
        if form.is_valid():
            form.save()
            group_id = groups.models.Group.objects.get(
                name=self.request.POST.get("name"),
            ).id
            user_id = self.request.user.id
            groups.models.GroupUser.objects.create(
                user_id=user_id,
                group_id=group_id,
                leader=1,
                moderator=0,
            )
            return django.shortcuts.redirect(
                django.shortcuts.reverse("groups:my"),
            )

        return django.shortcuts.render(
            self.request,
            "group/new_group.html",
            context,
        )


class GroupEnterUser(django.views.View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = {
                "title": "Присоединиться к группе",
                "form": groups.forms.EnterGroupForm(),
            }
            return django.shortcuts.render(
                self.request,
                "group/enter_group_name.html",
                context,
            )

        django.contrib.messages.info(self.request, "Вы не аутентифицированы")
        return django.shortcuts.redirect(
            django.shortcuts.reverse("homepage:main"),
        )

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = {
                "title": "Добавить пользователя в группу",
                "form": groups.forms.EnterGroupForm(),
            }
            try:
                group_id = groups.models.Group.objects.get(
                    name=self.request.POST.get("name"),
                ).id
            except django.core.exceptions.ObjectDoesNotExist:
                django.contrib.messages.error(
                    self.request,
                    "Такой группы не существует",
                )
                return django.shortcuts.render(
                    self.request,
                    "group/enter_group_name.html",
                    context,
                )

            if not groups.models.Group.objects.get(id=group_id).is_public:
                django.contrib.messages.error(
                    self.request,
                    "Группа приватная",
                )
                return django.shortcuts.render(
                    self.request,
                    "group/enter_group_name.html",
                    context,
                )

            user_id = self.request.user.id
            try:
                groups.models.GroupUser.objects.get(
                    user_id=user_id,
                    group_id=group_id,
                )
            except django.core.exceptions.ObjectDoesNotExist:
                pass
            else:
                django.contrib.messages.success(
                    self.request,
                    "Пользователь уже состоит в группе",
                )
                return django.shortcuts.redirect(
                    django.shortcuts.reverse("groups:enter_user_in_group"),
                )

            groups.models.GroupUser.objects.create(
                user_id=user_id,
                group_id=group_id,
                leader=0,
                moderator=0,
            )
            django.contrib.messages.success(
                self.request,
                "Вы были добавлены в группу" + self.request.POST.get("name"),
            )
            return django.shortcuts.redirect(
                django.shortcuts.reverse("groups:groups"),
            )

        django.contrib.messages.info(self.request, "Вы не аутентифицированы")
        return django.shortcuts.render(
            self.request,
            "homepage/main.html",
            {"title": "Главная"},
        )


class GroupInvitations(django.views.View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            invite = groups.models.GroupInvite.objects.filter(
                user=self.request.user.id,
            )
            context = {
                "title": "Приглашения",
                "invitation": invite.select_related(
                    "group",
                ).only("group_id"),
            }
            return django.shortcuts.render(
                self.request,
                "group/invitations.html",
                context,
            )

        django.contrib.messages.info(self.request, "Вы не аутентифицированы")
        return django.shortcuts.redirect(
            django.shortcuts.reverse("homepage:main"),
        )


class GroupInviteRequest(django.views.View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            contex = {
                "title": "Пригласить в группу",
                "form": groups.forms.InviteGroupForm(),
            }
            return django.shortcuts.render(
                self.request,
                "group/invite_request.html",
                contex,
            )

        django.contrib.messages.info(self.request, "Вы не аутентифицированы")
        return django.shortcuts.redirect(
            django.shortcuts.reverse("homepage:main"),
        )

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = {
                "title": "Пригласить в группу",
                "form": groups.forms.InviteGroupForm(),
            }
            form = groups.forms.InviteGroupForm(self.request.POST)
            if form.is_valid():
                try:
                    user = core.models.User.objects.get(
                        username=self.request.POST.get("user"),
                    )
                    group = groups.models.Group.objects.get(
                        id=kwargs.get("pk"),
                    )
                except django.core.exceptions.ObjectDoesNotExist:
                    django.contrib.messages.error(
                        self.request,
                        "Такого пользователя или группы не существует",
                    )
                    return django.shortcuts.render(
                        self.request,
                        "group/invite_request.html",
                        context,
                    )

                user_group = groups.models.GroupUser.objects.get(
                    user_id=self.request.user.id,
                    group_id=kwargs.get("pk"),
                )
                is_leader, is_moderator = (
                    user_group.leader,
                    user_group.moderator,
                )
                if not (is_leader or is_moderator):
                    django.contrib.messages.success(
                        self.request,
                        "Вы не являетесь ни лидером, ни модератором группы",
                    )
                    return django.shortcuts.redirect(
                        django.shortcuts.reverse("homepage:main"),
                    )

                try:
                    user_id = core.models.User.objects.get(
                        username=self.request.POST.get("user"),
                    ).id
                    groups.models.GroupUser.objects.get(
                        user_id=user_id,
                        group_id=kwargs.get("pk"),
                    )
                except django.core.exceptions.ObjectDoesNotExist:
                    pass
                else:
                    django.contrib.messages.success(
                        self.request,
                        "Пользователь уже состоит в группе",
                    )
                    return django.shortcuts.redirect(
                        django.shortcuts.reverse(
                            "groups:invite_request",
                            args=[kwargs.get("pk")],
                        ),
                    )

                groups.models.GroupInvite.objects.create(
                    user=user,
                    group=group,
                    text=self.request.POST.get("text"),
                )
                django.contrib.messages.success(self.request, "Удачно")
                return django.shortcuts.redirect(
                    django.shortcuts.reverse("homepage:main"),
                )

            django.contrib.messages.error(self.request, "Форма не валидна")
            return django.shortcuts.redirect(
                django.shortcuts.reverse(
                    "groups:invite_request",
                    args=[kwargs.get("pk")],
                ),
            )

        django.contrib.messages.info(self.request, "Вы не аутентифицированы")
        return django.shortcuts.redirect(
            django.shortcuts.reverse("homepage:main"),
        )


class GroupInviteCard(django.views.View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = {
                "title": "Приглашение",
                "context": groups.models.Group.objects.get(
                    id=kwargs.get("pk"),
                ),
                "form": groups.forms.AcceptRejectForm(),
            }
            return django.shortcuts.render(
                self.request,
                "group/invite_card.html",
                context,
            )

        django.contrib.messages.info(self.request, "Вы не аутентифицированы")
        return django.shortcuts.redirect(
            django.shortcuts.reverse("homepage:main"),
        )

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            context = {
                "title": "Приглашение",
                "context": groups.models.Group.objects.get(
                    id=kwargs.get("pk"),
                ),
                "form": groups.forms.AcceptRejectForm(),
            }
            form = groups.forms.AcceptRejectForm(self.request.POST)
            if form.is_valid():
                if self.request.POST.get("accept"):
                    groups.models.GroupUser.objects.create(
                        user_id=self.request.user.id,
                        group_id=kwargs.get("pk"),
                        leader=0,
                        moderator=0,
                    )
                    django.contrib.messages.success(
                        self.request,
                        "Вы успешно присоединились к группе",
                    )
                else:
                    django.contrib.messages.success(
                        self.request,
                        "Вы отклонили приглашение",
                    )

                groups.models.GroupInvite.objects.get(
                    group_id=kwargs.get("pk"),
                    user_id=self.request.user.id,
                ).delete()
                return django.shortcuts.redirect(
                    django.shortcuts.reverse("groups:invitations"),
                )

            django.contrib.messages.info(
                self.request,
                "Выберите вариант из предложенного списка",
            )
            return django.shortcuts.render(
                self.request,
                "group/invite_card.html",
                context,
            )

        django.contrib.messages.info(self.request, "Вы не аутентифицированы")
        return django.shortcuts.redirect(
            django.shortcuts.reverse("homepage:main"),
        )


__all__ = []
