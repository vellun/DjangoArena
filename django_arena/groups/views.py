import django.contrib.messages
import django.core.exceptions
import django.db.models
import django.shortcuts
import django.urls
import django.views

import groups.forms
import groups.models


class GroupView(django.views.View):
    def get(self, *args, **kwargs):
        sub_request = groups.models.GroupUser.objects.filter(
            user_id=self.request.user.id,  # TODO optimize
        ).only("group_id")
        list_group_id = [x.group_id for x in sub_request]
        request = groups.models.Group.objects.filter(
            id__in=list_group_id,
        ).only("name")
        context = {
            "title": "Группы",
            "groups": request,
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
            "title": "Группа",
            "group_form": form,
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
                django.shortcuts.reverse("groups:groups"),
            )

        return django.shortcuts.render(
            self.request,
            "group/new_group.html",
            context,
        )


class GroupEnterUser(django.views.View):
    def get(self, *args, **kwargs):
        context = {
            "title": "Главная",
        }
        if self.request.user.is_authenticated:
            context = {
                "title": "Добавить пользователя в группу",
                "form": groups.forms.EnterGroupForm(),
            }
            return django.shortcuts.render(
                self.request,
                "group/enter_group_name.html",
                context,
            )

        django.contrib.messages.info(self.request, "Вы не аутентифицированы")
        return django.shortcuts.render(
            self.request,
            "homepage/main.html",
            context,
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

            user_id = self.request.user.id
            groups.models.GroupUser.objects.create(
                user_id=user_id,
                group_id=group_id,
                leader=0,
                moderator=0,
            )
            django.contrib.messages.success(
                self.request,
                f"Вы были добавлены в группу {self.request.POST.get("name")}",
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


__all__ = []
