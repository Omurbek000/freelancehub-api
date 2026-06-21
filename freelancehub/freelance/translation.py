"""
Настройка переводов моделей (modeltranslation).

Определяет, какие поля моделей поддерживают переводы на несколько языков.
Языки: ru (русский), en (английский), ky (кыргызский).

Переводимые модели:
- Project — title, description, status
- Category — category_name
- Skill — skill_name
- Review — comment
- UserProfile — bio

modeltranslation автоматически создаёт поля:
- field_name_ru — русская версия
- field_name_en — английская версия
- field_name_ky — кыргызская версия
"""

from modeltranslation.translator import register, TranslationOptions
from .models import Project, Category, Skill, Offer, Review, UserProfile


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    """Перевод полей проекта: название, описание, статус."""
    fields = ('title', 'description', 'status')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    """Перевод названия категории."""
    fields = ('category_name',)


@register(Skill)
class SkillTranslationOptions(TranslationOptions):
    """Перевод названия навыка."""
    fields = ('skill_name',)


@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    """Перевод комментария в отзыве."""
    fields = ('comment',)


@register(UserProfile)
class UserProfileTranslationOptions(TranslationOptions):
    """Перевод биографии пользователя."""
    fields = ('bio',)
