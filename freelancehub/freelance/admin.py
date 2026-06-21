"""
Настройка админ-панели Django для моделей FreelanceHub.

Регистрирует все модели для управления через /admin/.
Использует TranslationAdmin для моделей с переводами (ru/en/ky).

Модели:
- Project — проекты (с фильтрацией по статусу/категории)
- Category — категории
- Skill — навыки
- Review — отзывы
- UserProfile — пользователи (с фильтрацией по роли)
- SocialLink — социальные ссылки
- Offer — предложения
"""

from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


@admin.register(Project)
class ProjectAdmin(TranslationAdmin):
    """Админка проектов с вкладками переводов (title_ru, title_en, title_ky)."""
    list_display = ['title', 'status', 'budget', 'client', 'created_at']  # Столбцы в списке
    list_filter = ['status', 'category']                                   # Фильтры в боковой панели
    search_fields = ['title', 'description']                               # Поиск по полям
    class Media:
        js = (
            "https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",
            "https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": ("modeltranslation/css/tabbed_translation_fields.css",),
        }


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    """Админка категорий с вкладками переводов."""
    list_display = ['category_name']
    search_fields = ['category_name']
    class Media:
        js = (
            "https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",
            "https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": ("modeltranslation/css/tabbed_translation_fields.css",),
        }


@admin.register(Skill)
class SkillAdmin(TranslationAdmin):
    """Админка навыков с вкладками переводов."""
    list_display = ['skill_name']
    search_fields = ['skill_name']
    class Media:
        js = (
            "https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",
            "https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": ("modeltranslation/css/tabbed_translation_fields.css",),
        }


@admin.register(Review)
class ReviewAdmin(TranslationAdmin):
    """Админка отзывов с фильтрацией по рейтингу."""
    list_display = ['reviewer', 'target', 'rating', 'project', 'created_at']
    list_filter = ['rating']
    class Media:
        js = (
            "https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",
            "https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": ("modeltranslation/css/tabbed_translation_fields.css",),
        }


@admin.register(UserProfile)
class UserProfileAdmin(TranslationAdmin):
    """Админка пользователей с фильтрацией по роли и статусу активности."""
    list_display = ['username', 'email', 'role', 'is_active']
    list_filter = ['role', 'is_active']
    search_fields = ['username', 'email']
    class Media:
        js = (
            "https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js",
            "https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": ("modeltranslation/css/tabbed_translation_fields.css",),
        }


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    """Админка социальных ссылок с фильтрацией по платформе."""
    list_display = ['user', 'platform', 'url']
    list_filter = ['platform']


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """Админка предложений с фильтрацией по проекту."""
    list_display = ['freelancer', 'project', 'proposed_budget', 'proposed_deadline', 'created_at']
    list_filter = ['project']
