from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"users-simple", UserProfileSimpleViewSet)
router.register(r"social-links", SocialLinkViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"projects", ProjectViewSet)
router.register(r"offers", OfferViewSet)
router.register(r"reviews", ReviewViewSet)

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", CustomLoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),

    path("users/", UserProfileListApiView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserProfileDetailApiView.as_view(), name="user-detail"),

    path("categories/<int:pk>/", CategoryDetailApiView.as_view(), name="category-detail"),

    path("projects-list/", ProjectListApiView.as_view(), name="project-list"),
    path("projects/<int:pk>/", ProjectDetailApiView.as_view(), name="project-detail"),

    path("offers-list/", OfferListApiView.as_view(), name="offer-list"),
    path("offers/<int:pk>/", OfferDetailApiView.as_view(), name="offer-detail"),

    path("", include(router.urls)),
]
