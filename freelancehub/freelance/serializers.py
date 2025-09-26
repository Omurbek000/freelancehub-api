from rest_framework import serializers
from .models import *


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "skill_name"]


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "first_name", "last_name", "role"]


class UserProfileListSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ["email", "skills"]


class UserProfileDetailSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ["email", "phone_number", "role", "bio", "avatar", "skills"]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
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
    refresh = serializers.CharField(required=True)

    def validate(self, data):
        refresh_token = data.get("refresh")
        try:
            token = RefreshToken(refresh_token)
            return data
        except TokenError:
            raise serializers.ValidationError({"detail": "Недействительный токен."})

    def save(self):
        refresh_token = self.validated_data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ["id", "user", "platform", "url"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "category_name"]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ProjectListSerializer(serializers.ModelSerializer):
    client = UserProfileSimpleSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ["title", "description", "budget", "deadline", "status", "client"]


class ProjectDetailSerializer(serializers.ModelSerializer):
    client = UserProfileSimpleSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    offer_freelancers = serializers.SerializerMethodField()

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
        offers = obj.offer_project.all()
        return OfferListSerializer(offers, many=True).data


class CategoryDetailSerializer(serializers.ModelSerializer):
    projects_category = ProjectListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["category_name", "projects_category"]


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"


class OfferListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ["message", "proposed_budget", "proposed_deadline", "created_at"]


class OfferDetailSerializer(serializers.ModelSerializer):
    offer_project = serializers.SerializerMethodField()
    offer_freelancer = serializers.SerializerMethodField()

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
        return ProjectListSerializer(obj.project).data

    def get_offer_freelancer(self, obj):
        return UserProfileSimpleSerializer(obj.freelancer).data


class ReviewSerializer(serializers.ModelSerializer):
    review_project = serializers.SerializerMethodField()
    reviewer_info = serializers.SerializerMethodField()
    target_info = serializers.SerializerMethodField()

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
        return ProjectListSerializer(obj.project).data

    def get_reviewer_info(self, obj):
        return UserProfileSimpleSerializer(obj.reviewer).data

    def get_target_info(self, obj):
        return UserProfileSimpleSerializer(obj.target).data
