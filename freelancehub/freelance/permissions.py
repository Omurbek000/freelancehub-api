from rest_framework import permissions


class CanCreateProject(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'client'


class CanCreateOffer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Freelancer'


class IsProjectOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.client


class IsReviewOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.reviewer
