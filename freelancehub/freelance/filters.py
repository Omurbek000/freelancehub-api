"""
Фильтры для DRF (django-filters).

Определяют параметры фильтрации для каждого эндпоинта.
Фронт может передавать параметры в URL для фильтрации результатов.

Примеры использования:
- /projects/?title__icontains=сайт — поиск по названию
- /projects/?budget__gte=1000&budget__lte=5000 — бюджет от 1000 до 5000
- /projects/?category=1 — фильтр по категории (ID=1)
- /offers/?freelancer=3 — предложения от фрилансера с ID=3
- /reviews/?rating__gte=4 — отзывы с рейтингом от 4
"""

from django_filters import FilterSet
from .models import Project, Offer, Review, UserProfile


class ProjectFilter(FilterSet):
    """
    Фильтр для проектов.
    Параметры:
    - title__icontains — поиск по названию (частичное совпадение, без учёта регистра)
    - description__icontains — поиск по описанию
    - category — точное совпадение по ID категории
    - budget__gte — бюджет >= значения
    - budget__lte — бюджет <= значения
    - skills — фильтр по навыку (ID)
    """
    class Meta:
        model = Project
        fields = {
            'title': ['icontains'],
            'description': ['icontains'],
            'category': ['exact'],
            'budget': ['gte', 'lte'],
            'skills': ['exact'],
        }


class OfferFilter(FilterSet):
    """
    Фильтр для предложений.
    Параметры:
    - freelancer — фильтр по ID фрилансера
    - project — фильтр по ID проекта
    - proposed_budget__gte — предложенный бюджет >= значения
    - proposed_budget__lte — предложенный бюджет <= значения
    - proposed_deadline — точная дата дедлайна
    """
    class Meta:
        model = Offer
        fields = {
            'freelancer': ['exact'],
            'project': ['exact'],
            'proposed_budget': ['gte', 'lte'],
            'proposed_deadline': ['exact'],
        }


class ReviewFilter(FilterSet):
    """
    Фильтр для отзывов.
    Параметры:
    - reviewer — фильтр по ID автора отзыва
    - target — фильтр по ID получателя отзыва
    - rating__gte — рейтинг >= значения
    - rating__lte — рейтинг <= значения
    - project — фильтр по ID проекта
    """
    class Meta:
        model = Review
        fields = {
            'reviewer': ['exact'],
            'target': ['exact'],
            'rating': ['gte', 'lte'],
            'project': ['exact'],
        }


class UserProfileFilter(FilterSet):
    """
    Фильтр для пользователей.
    Параметры:
    - email__icontains — поиск по email (частичное совпадение)
    - role — фильтр по роли (Freelancer/client/admin)
    - skills — фильтр по навыку (ID)
    """
    class Meta:
        model = UserProfile
        fields = {
            'email': ['icontains'],
            'role': ['exact'],
            'skills': ['exact'],
        }
