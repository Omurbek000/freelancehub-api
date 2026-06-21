"""
URL-маршруты приложения Freelance.

Router (автоматические CRUD-маршруты):
- /users-simple/ — пользователи (CRUD)
- /social-links/ — социальные ссылки (CRUD)
- /categories/ — категории (CRUD)
- /projects/ — проекты (CRUD)
- /offers/ — предложения (CRUD)
- /reviews/ — отзывы (CRUD)

Ручные маршруты:
- /register/ — регистрация нового пользователя
- /login/ — логин (получение JWT-токенов)
- /logout/ — выход (добавление refresh-токена в чёрный список)
- /user/ — список пользователей
- /user/<id>/ — профиль конкретного пользователя
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Router автоматически создаёт CRUD-маршруты для ViewSet'ов
router = DefaultRouter()
router.register(r"users-simple", UserProfileSimpleViewSet, basename='users-simple')  # /users-simple/
router.register(r"social-links", SocialLinkViewSet, basename='social-links')          # /social-links/
router.register(r"categories", CategoryViewSet, basename='categories')                # /categories/
router.register(r"projects", ProjectViewSet, basename='projects')                     # /projects/
router.register(r"offers", OfferViewSet, basename='offers')                           # /offers/
router.register(r"reviews", ReviewViewSet, basename='reviews')                        # /reviews/

urlpatterns = [
    # Аутентификация
    path('register/', RegisterView.as_view(), name='register'),        # POST /register/
    path('login/', CustomLoginView.as_view(), name='login'),           # POST /login/
    path('logout/', LogoutView.as_view(), name='logout'),              # POST /logout/

    # Пользователи
    path('user/', UserProfileListApiView.as_view(), name='user-list'),          # GET /user/
    path('user/<int:pk>/', UserProfileDetailApiView.as_view(), name='user-detail'),  # GET/PUT/PATCH/DELETE /user/<id>/

    # Все CRUD-маршруты из router
    path("", include(router.urls)),
]
