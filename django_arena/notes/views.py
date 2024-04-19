import django.contrib.auth.mixins
import django.shortcuts
import django.urls
import django.views.generic

import notes.forms
import notes.models


class NoteListAllView(django.views.generic.ListView):
    model = notes.models.Note
    template_name = "notes/note_list.html"
    context_object_name = "notes"
    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tab"] = "all"
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


__all__ = [NoteListAllView, NoteListMyView, NoteDetailView, NoteCreateView]
