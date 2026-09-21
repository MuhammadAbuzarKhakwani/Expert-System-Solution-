from rest_framework import permissions


class IsQuizCreator(permissions.BasePermission):
    """
    Custom permission to only allow creators to edit/delete their own quizzes.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the creator
        return obj.created_by == request.user
