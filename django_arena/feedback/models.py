from django.db import models


class Feedback(models.Model):
    class Status(models.TextChoices):
        RECEIVED = "received", "получено"
        PROGRESS = "progress", "в обработке"
        COMPLETE = "complete", "ответ дан"

    status = models.CharField(
        verbose_name="статус",
        db_column="status",
        max_length=20,
        choices=Status.choices,
        default=Status.RECEIVED,
    )

    text = models.CharField(
        verbose_name="текст",
        db_column="text",
        help_text="Напишите что-нибудь",
        max_length=300,
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
        null=True,
        db_column="created_on",
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"
