"""
Сериализаторы DRF для моделей FreelanceHub.

Сериализаторы преобразуют модели Django в JSON (и обратно) для REST API.

Сериализаторы:
- SkillSerializer — навыки
- RegisterSerializer — регистрация нового пользователя
- UserProfileSimpleSerializer — краткая информация о пользователе
- UserProfileListSerializer — пользователь для списка (с навыками)
- UserProfileDetailSerializer — полная информация о пользователе
- LoginSerializer — логин и выдача JWT-токенов
- LogoutSerializer — выход (чёрный список refresh-токена)
- SocialLinkSerializer — социальные ссылки
- CategorySerializer — категории
- CategoryDetailSerializer — категория с проектами
- ProjectSerializer — проект (все поля)
- ProjectListSerializer — проект для списка (с данными заказчика)
- ProjectDetailSerializer — полная информация о проекте (с предложениями)
- OfferSerializer — предложение (все поля)
- OfferListSerializer — краткое предложение
- OfferDetailSerializer — полная информация о предложении
- ReviewSerializer — отзыв с информацией о проекте и пользователях
"""

from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import TokenError


# ============================================================
# Навыки
# ============================================================

class SkillSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Skill (навыки)."""
    class Meta:
        model = Skill
        fields = ["id", "skill_name"]


# ============================================================
# Пользователи
# ============================================================

class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор регистрации нового пользователя.
    Принимает: username, email, password, first_name, last_name, role.
    Пароль хешируется через set_password() перед сохранением.
    """
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = UserProfile
        fields = ["username", "email", "password", "first_name", "last_name", "role"]

    def create(self, validated_data):
        """Создаёт пользователя с захешированным паролем."""
        user = UserProfile.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'client'),
        )
        return user


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    """
    Краткий сериализатор пользователя.
    Используется в списке пользователей и в составе других сериализаторов.
    """
    class Meta:
        model = UserProfile
        fields = ["id", "first_name", "last_name", "role"]


class UserProfileListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для списка пользователей.
    Включает навыки (вложенный сериализатор SkillSerializer).
    """
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ["email", "skills"]


class UserProfileDetailSerializer(serializers.ModelSerializer):
    """
    Детальный сериализатор пользователя.
    Включает: email, телефон, роль, биографию, аватар, навыки.
    """
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ["email", "phone_number", "role", "bio", "avatar", "skills"]


# ============================================================
# Аутентификация (Логин / Выход)
# ============================================================

class LoginSerializer(serializers.Serializer):
    """
    Сериализатор для логина.
    Принимает username и password, проверяет через authenticate().
    При успехе возвращает JWT-токены (access + refresh) и данные пользователя.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Проверяет учётные данные и возвращает объект пользователя."""
        username = data.get("username")
        password = data.get("password")
        user = UserProfile.objects.filter(username=username).first()
        if not user:
            raise serializers.ValidationError("Пользователь с таким username не найден")
        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError("Неверные учетные данные")
        return user

    def to_representation(self, instance):
        """Генерирует JWT-токены для успешно авторизованного пользователя."""
        refresh = RefreshToken.for_user(instance)
        return {
            "user": {
                "username": instance.username,
                "email": instance.email,
            },
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


class LogoutSerializer(serializers.Serializer):
    """
    Сериализатор для выхода (logout).
    Принимает refresh-токен и добавляет его в чёрный список,
    чтобы его нельзя было использовать повторно.
    """
    refresh = serializers.CharField(required=True)

    def validate(self, data):
        """Проверяет, что refresh-токен валиден."""
        refresh_token = data.get("refresh")
        try:
            token = RefreshToken(refresh_token)
            return data
        except TokenError:
            raise serializers.ValidationError({"detail": "Недействительный токен."})

    def save(self):
        """Добавляет refresh-токен в чёрный список."""
        refresh_token = self.validated_data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()


# ============================================================
# Социальные ссылки
# ============================================================

class SocialLinkSerializer(serializers.ModelSerializer):
    """Сериализатор для социальных ссылок пользователя (GitHub, Telegram и т.д.)."""
    class Meta:
        model = SocialLink
        fields = ["id", "user", "platform", "url"]


# ============================================================
# Категории
# ============================================================

class CategorySerializer(serializers.ModelSerializer):
    """Базовый сериализатор категории."""
    class Meta:
        model = Category
        fields = ["id", "category_name"]


# ============================================================
# Проекты
# ============================================================

class ProjectSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор проекта.
    Включает все поля модели. Используется для CRUD-операций.
    """
    class Meta:
        model = Project
        fields = '__all__'


class ProjectListSerializer(serializers.ModelSerializer):
    """
    Сериализатор проекта для списка.
    Включает вложенные данные о заказчике (UserProfileSimpleSerializer).
    """
    client = UserProfileSimpleSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ["title", "description", "budget", "deadline", "status", "client"]


class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    Детальный сериализатор проекта.
    Включает: заказчика, навыки, категорию и все предложения фрилансеров.
    """
    client = UserProfileSimpleSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    offer_freelancers = serializers.SerializerMethodField()  # Поля вычисляются динамически

    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "budget",
            "deadline",
            "status",
            "client",
            "category",
            "skills",
            "created_at",
            "offer_freelancers",
        ]

    def get_offer_freelancers(self, obj):
        """Возвращает список всех предложений для данного проекта."""
        offers = obj.offer_project.all()
        return OfferListSerializer(offers, many=True).data


class CategoryDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор категории с вложенными проектами.
    При запросе категории возвращает все проекты в этой категории.
    """
    projects_category = ProjectListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["category_name", "projects_category"]


# ============================================================
# Предложения (Offers)
# ============================================================

class OfferSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор предложения.
    Включает все поля модели. Используется для создания/обновления.
    """
    class Meta:
        model = Offer
        fields = "__all__"


class OfferListSerializer(serializers.ModelSerializer):
    """
    Краткий сериализатор предложения для списка.
    Включает только основную информацию без ссылок на проект/фрилансера.
    """
    class Meta:
        model = Offer
        fields = ["message", "proposed_budget", "proposed_deadline", "created_at"]


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Детальный сериализатор предложения.
    Включает вложенные данные о проекте и фрилансере.
    """
    offer_project = serializers.SerializerMethodField()       # Данные проекта
    offer_freelancer = serializers.SerializerMethodField()    # Данные фрилансера

    class Meta:
        model = Offer
        fields = [
            "message",
            "proposed_budget",
            "proposed_deadline",
            "created_at",
            "offer_project",
            "offer_freelancer",
        ]

    def get_offer_project(self, obj):
        """Возвращает информацию о проекте, на который сделано предложение."""
        return ProjectListSerializer(obj.project).data

    def get_offer_freelancer(self, obj):
        """Возвращает информацию о фрилансере, сделавшем предложение."""
        return UserProfileSimpleSerializer(obj.freelancer).data


# ============================================================
# Отзывы (Reviews)
# ============================================================

class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор отзыва.
    Включает вложенные данные о проекте, reviewer (кто оставил) и target (кому).
    """
    review_project = serializers.SerializerMethodField()   # Данные проекта
    reviewer_info = serializers.SerializerMethodField()    # Данные автора отзыва
    target_info = serializers.SerializerMethodField()      # Данные получателя отзыва

    class Meta:
        model = Review
        fields = [
            "rating",
            "comment",
            "created_at",
            "review_project",
            "reviewer_info",
            "target_info",
        ]

    def get_review_project(self, obj):
        """Возвращает информацию о проекте, к которому относится отзыв."""
        return ProjectListSerializer(obj.project).data

    def get_reviewer_info(self, obj):
        """Возвращает информацию об авторе отзыва."""
        return UserProfileSimpleSerializer(obj.reviewer).data

    def get_target_info(self, obj):
        """Возвращает информацию о получателе отзыва."""
        return UserProfileSimpleSerializer(obj.target).data
