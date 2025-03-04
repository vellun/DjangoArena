import achievements.models
import django.contrib.admin
import sorl.thumbnail.admin


class AchievementInline(
    sorl.thumbnail.admin.AdminImageMixin,
    django.contrib.admin.TabularInline,
):
    fields = [
        achievements.models.AchievementImage.image.field.name,
    ]
    model = achievements.models.AchievementImage


@django.contrib.admin.register(achievements.models.Achievement)
class AdminAchievements(django.contrib.admin.ModelAdmin):
    list_display = (
        achievements.models.Achievement.name.field.name,
        achievements.models.Achievement.description.field.name,
        achievements.models.Achievement.get_image,
    )
    list_display_links = (achievements.models.Achievement.name.field.name,)
    inlines = [
        AchievementInline,
    ]


__all__ = []
