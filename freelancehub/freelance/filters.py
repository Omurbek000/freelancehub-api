from django_filters import FilterSet
from .models import Project, Offer, Review, UserProfile


class ProjectFilter(FilterSet):
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
    class Meta:
        model = Offer
        fields = {
            'freelancer': ['exact'],
            'project': ['exact'],
            'proposed_budget': ['gte', 'lte'],
            'proposed_deadline': ['exact'],
        }


class ReviewFilter(FilterSet):
    class Meta:
        model = Review
        fields = {
            'reviewer': ['exact'],
            'target': ['exact'],
            'rating': ['gte', 'lte'],
            'project': ['exact'],
        }


class UserProfileFilter(FilterSet):
    class Meta:
        model = UserProfile
        fields = {
            'email': ['icontains'],
            'role': ['exact'],
            'skills': ['exact'],
        }
