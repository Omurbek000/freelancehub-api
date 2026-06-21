"""
Кастомная пагинация для DRF.

Определяет количество объектов на страницу и максимальный размер.
Используется в REST_FRAMEWORK['DEFAULT_PAGINATION_CLASS'] или в конкретных view.

Параметры:
- page_size — 3 объекта на страницу (по умолчанию)
- page_size_query_param — фронт может менять через ?page_size=10
- max_page_size — максимум 10 объектов на страницу
"""

from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 3                        # Количество объектов на одну страницу
    page_size_query_param = "page_size"  # Параметр URL для изменения размера страницы
    max_page_size = 10                   # Максимально допустимый размер страницы
