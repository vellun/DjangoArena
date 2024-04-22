import django.contrib.auth.models
import django.db.models


class UserManager(django.contrib.auth.models.BaseUserManager):
    def is_note_liked(self, note_id):
        return User.objects.filter(id=self.id, note_likes__id=note_id).exists()

    def is_note_disliked(self, note_id):
        return User.objects.filter(
            id=self.id,
            note_dislikes__id=note_id,
        ).exists()


class User(django.contrib.auth.models.AbstractUser):
    shortname = django.db.models.CharField(
        max_length=16,
        blank=True,
        null=True,
    )
    username = django.db.models.CharField(max_length=16, unique=True)
    rating = django.db.models.IntegerField(default=1000)
    views = django.db.models.PositiveIntegerField(default=0)
    friends = django.db.models.ManyToManyField(
        "self",
        blank=True,
    )
    github_link = django.db.models.URLField(blank=True, null=True)
    gitlab_link = django.db.models.URLField(blank=True, null=True)
    games_played = django.db.models.PositiveIntegerField(default=0)
    games_won = django.db.models.PositiveIntegerField(default=0)
    easy_problems = django.db.models.PositiveIntegerField(default=0)
    medium_problems = django.db.models.PositiveIntegerField(default=0)
    hard_problems = django.db.models.PositiveIntegerField(default=0)
    objects = UserManager()

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def get_user_rank(self):
        if self.rating < 1200:
            return "Новичок", "Разработчик рутуб"

        if 1200 <= self.rating < 1400:
            return "Ученик", "Чушпан"

        if 1400 <= self.rating < 1600:
            return "Специалист", "Отучился в яндекс лицее 1 год"

        if 1600 <= self.rating < 1900:
            return "Эксперт", "Отучился в яндекс лицее 2 год"

        if 1900 <= self.rating < 2200:
            return "Кандидат в мастера", "Отучился на джанго специализациях"

        if 2200 <= self.rating < 2300:
            return "Мастер", "Разработчик Г-компании"

        if 2300 <= self.rating < 2400:
            return "Международный мастер", "Пользователь арчлинукс"

        if 2400 <= self.rating < 2600:
            return "Гроссмейстер", "Закрыл 7 неделю на фулл"

        if 2600 <= self.rating < 2900:
            return "Международный гроссмейстер", "Любишь енотов"

        if 2900 <= self.rating < 3200:
            return "Легендарный гроссмейстер", "Разработчик телеграм"

        if self.rating >= 3200:
            return "Легенда платформы", "Прошёл курсы скилбокс"

        return "Экстраординарный случай", "Экстраординарный случай"


__all__ = [User]
