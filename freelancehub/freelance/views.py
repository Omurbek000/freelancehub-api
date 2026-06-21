"""
Представления (Views) API для FreelanceHub.

Эндпоинты аутентификации:
- RegisterView — регистрация нового пользователя
- CustomLoginView — логин (выдача JWT-токенов)
- LogoutView — выход (добавление refresh-токена в чёрный список)

Представления пользователей:
- UserProfileSimpleViewSet — CRUD пользователей (краткая информация)
- UserProfileListApiView — список всех пользователей (с навыками)
- UserProfileDetailApiView — профиль текущего пользователя

Представления социальных ссылок:
- SocialLinkViewSet — CRUD социальных ссылок

Представления категорий:
- CategoryViewSet — CRUD категорий
- CategoryDetailApiView — категория с проектами

Представления проектов:
- ProjectViewSet — CRUD проектов (с фильтрацией)
- ProjectListApiView — список проектов (публичный)
- ProjectDetailApiView — детали проекта (публичный)

Представления предложений:
- OfferViewSet — CRUD предложений (с фильтрацией)
- OfferListApiView — список предложений (публичный)
- OfferDetailApiView — детали предложения

Представления отзывов:
- ReviewViewSet — CRUD отзывов (с фильтрацией)
"""

from rest_framework import viewsets, generics, status, permissions
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import *
from .pagination import *
from .permissions import *
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


# ============================================================
# Аутентификация (Регистрация / Логин / Выход)
# ============================================================

class RegisterView(generics.CreateAPIView):
    """
    Регистрация нового пользователя.
    POST /register/
    Принимает: username, email, password, first_name, last_name, role.
    Доступно всем (без авторизации).
    Rate limit: 5/мин (настроено через throttle_classes если нужно).
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class CustomLoginView(TokenObtainPairView):
    """
    Кастомный логин с JWT-токенами.
    POST /login/
    Принимает: username, password.
    Возвращает: access-токен, refresh-токен, данные пользователя.
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail': 'неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    Выход из системы (чёрный список refresh-токена).
    POST /logout/
    Принимает: refresh (refresh-токен).
    После вызова refresh-токен становится недействительным.
    """
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'detail': 'Refresh токен не предоставлен.'}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Вы успешно вышли.'}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({'detail': 'Недействительный токен.'}, status=status.HTTP_400_BAD_REQUEST)


# ============================================================
# Пользователи
# ============================================================

class UserProfileSimpleViewSet(viewsets.ModelViewSet):
    """
    CRUD-операции с пользователями (краткая информация).
    Router: /users-simple/
    Поддерживает: фильтрацию, поиск, сортировку.
    Требует авторизацию.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSimpleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = UserProfileFilter
    ordering_fields = ['username', 'email']
    search_fields = ['username', 'email']


class UserProfileListApiView(generics.ListAPIView):
    """
    Список всех пользователей (с навыками).
    GET /user/
    Требует авторизацию.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer
    permission_classes = [IsAuthenticated]


class UserProfileDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    Профиль текущего пользователя (retrieve/update/delete).
    GET/PUT/PATCH/DELETE /user/<id>/
    Пользователь видит/редактирует только свой профиль.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer

    def get_queryset(self):
        """Возвращает только профиль текущего авторизованного пользователя."""
        if self.request.user.is_authenticated:
            return UserProfile.objects.filter(id=self.request.user.id)
        return UserProfile.objects.none()


# ============================================================
# Социальные ссылки
# ============================================================

class SocialLinkViewSet(viewsets.ModelViewSet):
    """
    CRUD-операции с социальными ссылками.
    Router: /social-links/
    Требует авторизацию.
    """
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer
    permission_classes = [IsAuthenticated]


# ============================================================
# Категории
# ============================================================

class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD-операции с категориями.
    Router: /categories/
    Требует авторизацию.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class CategoryDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    Детальная информация о категории (с проектами).
    GET/PUT/PATCH/DELETE /category/<id>/
    Требует авторизацию.
    """
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsAuthenticated]


# ============================================================
# Проекты
# ============================================================

class ProjectViewSet(viewsets.ModelViewSet):
    """
    CRUD-операции с проектами.
    Router: /projects/
    Поддерживает: фильтрацию по названию, описанию, категории, бюджету, навыкам.
    Поддерживает: поиск и сортировку.
    Требует авторизацию.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProjectFilter
    ordering_fields = ['title', 'budget', 'created_at']
    search_fields = ['title', 'description']


class ProjectListApiView(generics.ListAPIView):
    """
    Публичный список проектов (без авторизации).
    GET /project/
    Используется фронтом для отображения списка проектов.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    permission_classes = [permissions.AllowAny]


class ProjectDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    Публичный детальный просмотр проекта.
    GET /project/<id>/
    Включает информацию о заказчике, навыках, категории и все предложения.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = [permissions.AllowAny]


# ============================================================
# Предложения (Offers)
# ============================================================

class OfferViewSet(viewsets.ModelViewSet):
    """
    CRUD-операции с предложениями.
    Router: /offers/
    Поддерживает: фильтрацию по фрилансеру, проекту, бюджету, дедлайну.
    Требует авторизацию.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = OfferFilter
    ordering_fields = ['proposed_budget', 'proposed_deadline']
    search_fields = ['message']


class OfferListApiView(generics.ListAPIView):
    """
    Публичный список предложений.
    GET /offer/
    """
    queryset = Offer.objects.all()
    serializer_class = OfferListSerializer
    permission_classes = [permissions.AllowAny]


class OfferDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """
    Детальная информация о предложении.
    GET/PUT/PATCH/DELETE /offer/<id>/
    Включает информацию о проекте и фрилансере.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]


# ============================================================
# Отзывы (Reviews)
# ============================================================

class ReviewViewSet(viewsets.ModelViewSet):
    """
    CRUD-операция с отзывами.
    Router: /reviews/
    Поддерживает: фильтрацию по reviewer, target, рейтингу, проекту.
    Поддерживает: поиск по комментариям.
    Требует авторизацию.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ['rating', 'created_at']
    search_fields = ['comment']
