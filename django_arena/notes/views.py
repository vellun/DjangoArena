from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import django.views.generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

import notes.forms
import notes.models


class NoteListView(django.views.generic.ListView):
    model = notes.models.Note
    template_name = "notes/note_list.html"
    context_object_name = "notes"
    ordering = ["-created_at"]


class NoteDetailView(django.views.generic.DetailView):
    model = notes.models.Note
    template_name = "notes/post_detail.html"


class NoteCreateView(LoginRequiredMixin, django.views.generic.CreateView):
    model = notes.models.Note
    template_name = "notes/note_create.html"
    form_class = notes.forms.NoteForm

    def get_success_url(self):
        return reverse("homepage:main")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# class PostUpdateView(
#     LoginRequiredMixin, UserPassesTestMixin, django.views.generic.UpdateView
# ):
#     model = Post
#     template_name = "notes/post_update.html"
#     fields = ["title", "content"]

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

#     def test_func(self):
#         post = self.get_object()
#         return self.request.user == post.author


# class PostDeleteView(
#     LoginRequiredMixin, UserPassesTestMixin, django.views.generic.DeleteView
# ):
#     model = Post
#     template_name = "notes/post_delete.html"
#     success_url = "/"

#     def test_func(self):
#         post = self.get_object()
#         return self.request.user == post.author

__all__ = [NoteListView, NoteDetailView, NoteCreateView]
