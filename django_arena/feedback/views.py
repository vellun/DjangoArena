import django.conf
import django.contrib
import django.core.mail
import django.shortcuts

from feedback.forms import FeedbackForm


class FeedbackView(django.views.View):
    def dispatch(self, request, *args, **kwargs):
        self.feedback_form = FeedbackForm(request.POST or None)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {
            "title": "Отзыв",
            "form": self.feedback_form,
        }

        return django.shortcuts.render(
            request,
            "feedback/feedback.html",
            context,
        )

    def post(self, request):
        if self.feedback_form.is_valid():
            self.feedback_form.save()
            django.contrib.messages.success(
                request,
                "Ваш отзыв успешно отправлен!",
            )

            return django.shortcuts.redirect(request.path)

        return self.get(request)


__all__ = []
