from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter , OrderingFilter
from .filters import *
from .pagination import *
from .permissions import *
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    serializer_class = UserProfileSimpleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail':' неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'detail': 'Refresh токен не предоставлен.'}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Вы успешно вышли.'}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({'detail': 'Недействительный токен.'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileSimpleViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSimpleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = UserProfileFilter
    ordering_fields = ['username', 'email']
    search_fields = ['username', 'email']

class UserProfileListApiView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer
    

class UserProfileDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer
    
    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class SocialLinkViewSet(viewsets.ModelViewSet):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [CanCreateProject, IsProjectOwner]
    filter_backends = [DjangoFilterBackend , SearchFilter , OrderingFilter]
    filterset_class = ProjectFilter
    ordering_fields = ['category', 'title', 'budget','skills', 'description']
    search_fields = ['title', 'description', 'category', 'budget', 'skills']

class ProjectListApiView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer

class ProjectDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [CanCreateOffer]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = OfferFilter
    ordering_fields = ['freelancer', 'project','proposed_budget', 'proposed_deadline',]
    search_fields = ['freelanсer', 'project', 'proposed_budget', 'proposed_deadline',]

class OfferListViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferListSerializer

class OfferDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferDetailSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewOwner]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ['reviewer', 'target', 'project', 'rating',]
    search_fields = ['reviewer', 'target', 'project', 'rating',]