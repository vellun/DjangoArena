import django.db.models
import django.utils.safestring
import sorl.thumbnail

import core.models


class Achievement(django.db.models.Model):
    name = django.db.models.CharField(max_length=255)
    description = django.db.models.TextField()
    created_at = django.db.models.DateTimeField(
        auto_now=True,
    )
    user_id = django.db.models.ManyToManyField(
        core.models.User,
        related_name="achievements",
        related_query_name="achievements",
    )

    def get_image(self):
        image = AchievementImage.objects.get(achievement=self.id)
        return django.utils.safestring.mark_safe(
            f"<image src='{image.get_image300x300().url}'>",
        )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"


class AchievementImage(django.db.models.Model):
    image = django.db.models.ImageField(
        upload_to="image/achievements/",
        null=False,
    )
    achievement = django.db.models.OneToOneField(
        Achievement,
        on_delete=django.db.models.CASCADE,
        related_name="image",
        related_query_name="image",
    )

    def get_image300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            geometry_string="300x300",
            crop="center",
            quality=51,
        )

    def image_tmb(self):
        if self.image:
            tag = f"<image src='{self.get_image300x300().url}'>"
            return django.utils.safestring.mark_safe(tag)

        return "Картинку не нашли("

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинка"


__all__ = ["Achievement", "AchievementImage"]
