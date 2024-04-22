import django.http
import django.views.decorators.http

import core.models
import users.forms


class ProfileView(django.views.View):
    def get(self, *args, **kwargs):
        user_id = kwargs.get("user_id")
        user = django.shortcuts.get_object_or_404(core.models.User, pk=user_id)
        user_rank = user.get_user_rank()
        user_rank_distribution = [
            core.models.User.objects.filter(id__gte=0, id__lt=1200).count(),
            core.models.User.objects.filter(id__gte=1200, id__lt=1400).count(),
            core.models.User.objects.filter(id__gte=1400, id__lt=1600).count(),
            core.models.User.objects.filter(id__gte=1600, id__lt=1900).count(),
            core.models.User.objects.filter(id__gte=1900, id__lt=2200).count(),
            core.models.User.objects.filter(id__gte=2200, id__lt=2300).count(),
            core.models.User.objects.filter(id__gte=2300, id__lt=2400).count(),
            core.models.User.objects.filter(id__gte=2400, id__lt=2600).count(),
            core.models.User.objects.filter(id__gte=2600, id__lt=2900).count(),
            core.models.User.objects.filter(id__gte=2900, id__lt=3200).count(),
            core.models.User.objects.filter(id__gte=3200).count(),
        ]
        context = {
            "title": "Профиль",
            "user": user,
            "user_rank": user_rank,
            "user_rank_distribution": user_rank_distribution,
        }
        return django.shortcuts.render(
            self.request,
            "users/profile.html",
            context,
        )


class SignupView(django.views.View):
    def get(self, request):
        form = users.forms.SignUpForm(request.POST or None)
        template = "users/signup.html"
        context = {
            "form": form,
        }
        return django.shortcuts.render(request, template, context)

    def post(self, request):
        form = users.forms.SignUpForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            django.contrib.messages.success(
                request,
                "Вы успешно зарегистрированы",
            )

            return django.shortcuts.redirect(
                django.urls.reverse("users:login"),
            )

        return self.get(request)


class CustomLoginView(django.contrib.auth.views.LoginView):
    def form_invalid(self, form):
        user = core.models.User.objects.get_by_natural_key(
            form.cleaned_data["username"],
        )

        if (
            user is not None
            and hasattr(user, "profile")
            and user.profile.attempts_count
            >= django.conf.settings.MAX_AUTH_ATTEMPTS
        ):
            return django.http.HttpResponseRedirect(
                django.urls.reverse(
                    "users:deactivate",
                    kwargs={"username": user.username},
                ),
            )

        return super().form_invalid(form)


__all__ = []
