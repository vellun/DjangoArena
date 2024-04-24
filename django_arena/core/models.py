import datetime
import pathlib
import uuid

import django.contrib.auth.models
import django.core.exceptions
import django.db.models
import pytz


def valid_birthday(value):
    if value > datetime.datetime.now(pytz.utc).date():
        raise django.core.exceptions.ValidationError(
            message="""Путешествий во времени не бывает!
            Или..кхм, в любом случае, вернитесь в настоящее
            и укажите корректную дату рождения!""",
        )


def get_path_image(instance, filename):
    file_extension = pathlib.Path(filename).suffix
    return f"users/{uuid.uuid4()}{file_extension}"


class User(django.contrib.auth.models.AbstractUser):
    shortname = django.db.models.CharField(
        verbose_name="имя",
        help_text="Введите свое имя(настояшее или вымышленное, \
            главное - чемпионское)",
        max_length=16,
        blank=True,
        null=True,
    )
    birthday = django.db.models.DateField(
        "дата рождения",
        help_text="Укажите дату рождения",
        null=True,
        blank=True,
        validators=[valid_birthday],
    )
    username = django.db.models.CharField(
        verbose_name="имя пользователя",
        help_text="Придумайте уникальное имя пользователя",
        max_length=16,
        unique=True,
    )
    image = django.db.models.ImageField(
        "аватарка",
        help_text="Загрузите аватарку",
        upload_to=get_path_image,
        null=True,
        blank=True,
    )
    rating = django.db.models.IntegerField(default=1000)
    views = django.db.models.PositiveIntegerField(default=0)
    friends = django.db.models.ManyToManyField(
        "self",
        blank=True,
    )
    github_link = django.db.models.URLField(
        verbose_name="ссылка на ваш github",
        blank=True,
        null=True,
    )
    gitlab_link = django.db.models.URLField(
        verbose_name="ссылка на ваш gitlab",
        blank=True,
        null=True,
    )
    games_played = django.db.models.PositiveIntegerField(default=0)
    games_won = django.db.models.PositiveIntegerField(default=0)
    easy_problems = django.db.models.PositiveIntegerField(default=0)
    medium_problems = django.db.models.PositiveIntegerField(default=0)
    hard_problems = django.db.models.PositiveIntegerField(default=0)

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
