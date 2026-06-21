from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta

# ============================================================
# FreelanceHub API — Настройки Django проекта
# ============================================================

# Базовая директория проекта (freelancehub/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Загрузка переменных окружения из .env файла
load_dotenv()

# Секретный ключ приложения (хранится в .env)
SECRET_KEY = os.getenv('SECRET_KEY',)

# Режим отладки (False в продакшене)
DEBUG = False

# Разрешённые хосты (в продакшене указать конкретные домены)
ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# ============================================================
# Установленные приложения
# ============================================================
INSTALLED_APPS = [
    'modeltranslation',              # Поддержка переводов моделей (ru/en/ky)
    'django.contrib.admin',          # Админ-панель Django
    'django.contrib.auth',           # Система аутентификации
    'django.contrib.contenttypes',   # Типы контента (нужен для auth)
    'django.contrib.sessions',       # Сессии
    'django.contrib.messages',       # Система сообщений
    'django.contrib.staticfiles',    # Статические файлы (CSS, JS, изображения)
    'rest_framework',                # Django REST Framework — REST API
    'freelance',                     # Основное приложение фриланс-платформы
    'phonenumber_field',             # Валидация и хранение номеров телефонов
    'django_filters',                # Фильтрация queryset'ов в DRF
    'drf_yasg',                      # Автогенерация Swagger/OpenAPI документации
    'allauth',                       # django-allauth — аутентификация через соцсети
    'allauth.account',               # Базовая аккаунтная система allauth
    'allauth.socialaccount',         # Социальные аккаунты (GitHub, Google)
    'allauth.socialaccount.providers.github',  # Авторизация через GitHub
    'allauth.socialaccount.providers.google',  # Авторизация через Google
    'rest_framework_simplejwt',      # JWT-токены (access + refresh)
    'rest_framework_simplejwt.token_blacklist', # Чёрный список JWT (для logout)
]


# ============================================================
# Промежуточные слои (Middleware)
# ============================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',           # Безопасность (HTTPS-заголовки)
    'django.contrib.sessions.middleware.SessionMiddleware',    # Обработка сессий
    'django.middleware.common.CommonMiddleware',               # Базовые проверки ( trailing slash)
    'django.middleware.csrf.CsrfViewMiddleware',              # Защита от CSRF-атак
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Привязка пользователя к запросу
    'django.contrib.messages.middleware.MessageMiddleware',    # Обработка сообщений
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Защита от clickjacking
    'django.middleware.locale.LocaleMiddleware',               # Определение языка из URL/заголовков
    "allauth.account.middleware.AccountMiddleware",            # Интеграция allauth с сессиями
]


# ============================================================
# Шаблоны
# ============================================================
ROOT_URLCONF = 'freelancehub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',   # Доступ к request в шаблонах
                'django.contrib.auth.context_processors.auth',  # Доступ к user в шаблонах
                'django.contrib.messages.context_processors.messages',  # Сообщения
            ],
        },
    },
]

WSGI_APPLICATION = 'freelancehub.wsgi.application'


# ============================================================
# База данных (SQLite для разработки)
# ============================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ============================================================
# Валидация паролей
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},  # Пароль не похож на имя/email
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},              # Минимум 8 символов
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},             # Нельзя использовать "password123"
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},            # Нельзя только цифры
]


# ============================================================
# Интернационализация (i18n)
# ============================================================
LANGUAGE_CODE = 'ru'       # Язык по умолчанию — русский
TIME_ZONE = 'UTC'          # Часовой пояс
USE_I18N = True            # Включить переводы
USE_L10N = True            # Включить локализацию дат/чисел
USE_TZ = True              # Использовать aware datetime

# Поддерживаемые языки
LANGUAGES = (
    ('ru', 'Русский'),
    ('en', 'English'),
    ('ky', 'Кыргызча'),
)

# Язык по умолчанию для modeltranslation
MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'


# ============================================================
# Статические и медиа файлы
# ============================================================
STATIC_URL = 'static/'                             # URL-префикс для статики
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Куда собирать статику (collectstatic)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')       # Куда сохранять загруженные файлы
MEDIA_URL = '/media/'                              # URL-префикс для медиа


# ============================================================
# Модель пользователя по умолчанию
# ============================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Кастомная модель пользователя вместо стандартной auth.User
AUTH_USER_MODEL = 'freelance.UserProfile'


# ============================================================
# Django REST Framework — общие настройки
# ============================================================
REST_FRAMEWORK = {
    # Бэкенд фильтрации (django-filters)
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],

    # Пагинация по умолчанию (3 объекта на страницу)
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 3,

    # Аутентификация по умолчанию — JWT-токены
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    # Rate limiting (ограничение количества запросов)
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',  # Анонимные пользователи
        'rest_framework.throttling.UserRateThrottle',   # Авторизованные пользователи
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',       # Анонимы: 100 запросов в час
        'user': '1000/hour',      # Авторизованные: 1000 запросов в час
        'login': '5/minute',      # Логин/регистрация: 5 попыток в минуту
    },
}


# ============================================================
# Бэкенды аутентификации
# ============================================================
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',             # Стандартная аутентификация (username/password)
    'allauth.account.auth_backends.AuthenticationBackend',  # Социальная аутентификация (GitHub, Google)
]


# ============================================================
# Email (вывод в консоль для разработки)
# ============================================================
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# ============================================================
# Simple JWT — настройки токенов
# ============================================================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),  # Access-токен живёт 30 минут
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),     # Refresh-токен живёт 7 дней
    "ROTATE_REFRESH_TOKENS": False,                  # Не выдавать новый refresh при обновлении
    "BLACKLIST_AFTER_ROTATION": False,                # Не добавлять в чёрный список после ротации
    "AUTH_HEADER_TYPES": ("Bearer",),                 # Формат заголовка: Authorization: Bearer <token>
}
