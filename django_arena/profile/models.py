from django.db import models
import django.conf


class CustomProfile(models.Model):
    user = models.OneToOneField(
        django.conf.settings.AUTH_USER_MODEL,
        verbose_name="пользователь",
        help_text="Укажите пользователя",
        related_name="profile",
        related_query_name="profile",
        on_delete=django.db.models.CASCADE,
        null=True,
        blank=True,
    )


class Achievements(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    filename = models.ImageField(
        upload_to="achievements/",
        null=True,
        blank=True,
    )
    user_id = models.ForeignKey(
        CustomProfile,
        related_name="achievements",
        related_query_name="achievements",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )


class Problem(models.Model):
    choices = ((1, "hard_reject"),
               (2, "soft_reject"),
               (3, "accept"),
               )
    title = models.CharField(max_length=255)
    tests_file = models.FileField(
        upload_to="problem/tests/"
    )
    answer_file = models.FileField(
        upload_to="problem/answer/"
    )
    status = models.TextField(
        choices=choices,
    )
    hard_reject_accumulation = models.IntegerField(
        default=0,
    )
    day_task = models.BooleanField(
        default=False,
    )
    week_task = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    user_id = models.ManyToManyField(
        CustomProfile,
        related_name="problem",
        related_query_name="problem",
    )
