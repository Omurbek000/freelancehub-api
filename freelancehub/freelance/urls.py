from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"users-simple", UserProfileSimpleViewSet, basename='users-simple') 
router.register(r"social-links", SocialLinkViewSet, basename='social-links')
router.register(r"categories", CategoryViewSet, basename='categories')
router.register(r"projects", ProjectViewSet, basename='projects')
router.register(r"offers", OfferViewSet, basename='offers')
router.register(r"reviews", ReviewViewSet, basename='reviews')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserProfileListApiView.as_view(), name='user'),
    path('user/<int:pk>/', UserProfileDetailApiView.as_view(), name='user-detail'),
    path('category/<int:pk>/', CategoryDetailApiView.as_view(), name='category-detail'),
    path('project/', ProjectListApiView.as_view(), name='project'),
    path('project/<int:pk>/', ProjectDetailApiView.as_view(), name='project-detail'),
    path('offer/', OfferListApiView.as_view(), name='offer'),
    path('offer/<int:pk>/', OfferDetailApiView.as_view(), name='offer-detail'),
    path("", include(router.urls)),
]
