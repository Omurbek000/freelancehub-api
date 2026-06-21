"""
Кастомные классы разрешений (permissions) для DRF.

Определяют, кто может просматривать/создавать/изменять данные.

Классы:
- IsAuthenticated — требует авторизацию (любой залогиненный пользователь)
- CanCreateProject — только заказчики (client) могут создавать проекты
- CanCreateOffer — только фрилансеры (Freelancer) могут создавать предложения
- IsProjectOwner — только владелец проекта может редактировать/удалять его
- IsReviewOwner — только автор отзыва может редактировать/удалять его
"""

from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):
    """
    Разрешает доступ только авторизованным пользователям.
    Используется на большинстве эндпоинтов (ViewSet'ы, Detail-представления).
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class CanCreateProject(permissions.BasePermission):
    """
    Разрешает создание проектов только пользователям с ролью 'client'.
    Используется на ProjectViewSet.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'client'


class CanCreateOffer(permissions.BasePermission):
    """
    Разрешает создание предложений только пользователям с ролью 'Freelancer'.
    Используется на OfferViewSet.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Freelancer'


class IsProjectOwner(permissions.BasePermission):
    """
    Разрешает изменение/удаление проекта только его владельцу (client).
    Проверяется на уровне объекта (has_object_permission).
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.client


class IsReviewOwner(permissions.BasePermission):
    """
    Разрешает изменение/удаление отзыва только его автору (reviewer).
    Проверяется на уровне объекта (has_object_permission).
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.reviewer
