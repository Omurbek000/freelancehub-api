"""
Корневые URL-маршруты проекта FreelanceHub.

Маршруты:
- /admin/ — админ-панель Django
- / — все URL приложения freelance (аутентификация, CRUD)
- /docs/ — Swagger UI (автогенерированная документация API)
- /accounts/ — allauth (социальная аутентификация: GitHub, Google)
- /media/ — загруженные файлы (аватары, изображения)
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Настройка Swagger/OpenAPI документации
schema_view = get_schema_view(
    openapi.Info(
        title="FreelanceHub API",
        default_version='v1',),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),                                           # Админ-панель
    path('', include('freelance.urls')),                                       # API endpoints
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger UI
    path('accounts/', include('allauth.urls')),                                # Allauth (social auth)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)             # Медиа-файлы
