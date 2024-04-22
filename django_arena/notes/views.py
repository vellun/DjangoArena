import django.contrib.auth.mixins
import django.shortcuts
import django.urls
import django.views.generic
import django.http

import notes.forms
import notes.models
import core.models


class NoteListAllView(django.views.generic.ListView):
    model = notes.models.Note
    template_name = "notes/note_list.html"
    context_object_name = "notes"
    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tab"] = "all"
        context["title"] = "Блог: популярное"
        return context


class NoteListMyView(django.views.generic.ListView):
    model = notes.models.Note
    template_name = "notes/note_list.html"
    context_object_name = "notes"
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author_id=self.request.user.id).order_by(
            "-created_at",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tab"] = "my"
        context["title"] = "Блог: мои посты"
        return context


class NoteDetailView(django.views.generic.DetailView):
    model = notes.models.Note
    template_name = "notes/note_detail.html"
    context_object_name = "note"


class NoteCreateView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.CreateView,
):
    model = notes.models.Note
    template_name = "notes/note_create.html"
    form_class = notes.forms.NoteForm
    success_url = django.urls.reverse_lazy("notes:blog-my")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NoteUpdateView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.contrib.auth.mixins.UserPassesTestMixin,
    django.views.generic.UpdateView,
):
    model = notes.models.Note
    template_name = "notes/note_create.html"
    form_class = notes.forms.NoteForm
    pk_url_kwarg = "pk"
    success_url = django.urls.reverse_lazy("notes:blog-my")

    def test_func(self):
        note = self.get_object()
        return self.request.user == note.author


class NoteDeleteView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.contrib.auth.mixins.UserPassesTestMixin,
    django.views.generic.DeleteView,
):
    model = notes.models.Note
    template_name = "notes/note_confirm_delete.html"
    pk_url_kwarg = "pk"
    success_url = django.urls.reverse_lazy("notes:blog-my")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class NoteLikeView(django.views.View):
    def post(self, *args, **kwargs):
        note_id = self.request.POST.get("note_id")
        user_id = self.request.POST.get("user_id")
        note = notes.models.Note.objects.get(id=note_id)
        user = core.models.User.objects.get(id=user_id)
        if notes.models.Note.objects.filter(id=note.id, user_dislikes__id=user.id).exists():
            note.user_dislikes.remove(user)
            note.dislikes -= 1
            note.save()
        if notes.models.Note.objects.filter(id=note.id, user_likes__id=user.id).exists():
            return django.http.HttpResponse("Already liked", status=400)
        note.user_likes.add(user)
        note.likes += 1
        note.save()
        return django.http.HttpResponse("Liked successfully", status=200)


class NoteDislikeView(django.views.View):
    def post(self, *args, **kwargs):
        note_id = self.request.POST.get("note_id")
        user_id = self.request.POST.get("user_id")
        note = notes.models.Note.objects.get(id=note_id)
        user = core.models.User.objects.get(id=user_id)
        if notes.models.Note.objects.filter(id=note.id, user_likes__id=user.id).exists():
            note.user_likes.remove(user)
            note.likes -= 1
            note.save()
        if notes.models.Note.objects.filter(id=note.id, user_dislikes__id=user.id).exists():
            return django.http.HttpResponse("Already disliked", status=400)
        note.user_dislikes.add(user)
        note.dislikes += 1
        note.save()
        return django.http.HttpResponse("Disliked successfully", status=200)


__all__ = []
