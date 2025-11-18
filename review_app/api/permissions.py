from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.exceptions import NotFound, PermissionDenied

class ReviewPermissions(BasePermission):
    """
    Custom permission to allow:
    - Anyone with authentication to read (GET, HEAD, OPTIONS)
    - Reviewer to update (PUT, PATCH) his own review only
    - Permission for POST (Customer users) or DELETE (review creator)
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        elif request.method == 'POST':
            return request.user and request.user.is_authenticated and request.user.type == 'customer'
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user and request.user.is_authenticated
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.reviewer == request.user and request.user and request.user.is_authenticated and request.user.type == 'customer'
        return False