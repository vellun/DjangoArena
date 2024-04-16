from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    shortname = models.CharField(max_length=16, blank=True, null=True)
    rating = models.IntegerField(default=1000)
    views = models.PositiveIntegerField(default=0)
    friends = models.ManyToManyField(
        "self",
        blank=True,
    )
    github_link = models.URLField(blank=True, null=True)
    gitlab_link = models.URLField(blank=True, null=True)
    games_played = models.PositiveIntegerField(default=0)
    games_won = models.PositiveIntegerField(default=0)
    easy_problems = models.PositiveIntegerField(default=0)
    medium_problems = models.PositiveIntegerField(default=0)
    hard_problems = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return f"{self.username}"


__all__ = [User]
