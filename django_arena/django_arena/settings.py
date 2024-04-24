import os
from pathlib import Path

import dotenv

dotenv.load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", default="reallysecret")

TRUE_VALUES = (
    "true",
    "yes",
    "1",
    "y",
)

DEBUG = os.getenv("DJANGO_DEBUG", default="False").lower() in TRUE_VALUES

ALLOWED_HOSTS = os.getenv(
    "DJANGO_ALLOWED_HOSTS",
    default="localhost,127.0.0.1,[::1]",
).split(",")

INSTALLED_APPS = [
    # Should be in start
    "daphne",
    # Own applications
    "core.apps.CoreConfig",
    "notifications.apps.NotificationsConfig",
    "homepage.apps.HomepageConfig",
    "problems.apps.ProblemsConfig",
    "groups.apps.GroupsConfig",
    "chatrooms.apps.ChatroomsConfig",
    "achievements.apps.AchievementsConfig",
    "notes.apps.NoteConfig",
    "tags.apps.TagsConfig",
    "users.apps.UsersConfig",
    "duel.apps.DuelConfig",
    "submissions.apps.SubmissionsConfig",
    "lobby.apps.LobbyConfig",
    # Django applications
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sorl.thumbnail",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    INTERNAL_IPS = [
        "localhost",
        "127.0.0.1",
    ]
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    INSTALLED_APPS.append("debug_toolbar")

ROOT_URLCONF = "django_arena.urls"

TEMPLATES_DIRS = [BASE_DIR / "templates"]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": TEMPLATES_DIRS,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "notifications.context_processors.get_notifications",
            ],
        },
    },
]

WSGI_APPLICATION = "django_arena.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth."
        "password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth."
        "password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth."
        "password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth."
        "password_validation.NumericPasswordValidator",
    },
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

ASGI_APPLICATION = "django_arena.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/auth/login/"

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static_dev",
]

LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/auth/login/"

STATICFILES_DIRS = [
    BASE_DIR / "static_dev",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "core.User"

ARENA_TESTING_HOST = "localhost:8001"

LOGIN_URL = "/users/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
