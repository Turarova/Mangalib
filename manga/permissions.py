from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCommentAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.user


