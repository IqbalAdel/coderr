from rest_framework import permissions

class ProfileEditPermission(permissions.BasePermission):
    """
    Custom permission to allow:
    - Anyone with authentication to read (GET, HEAD, OPTIONS)
    - User to update (PUT, PATCH) his own profile only
    - No permission for POST or DELETE 
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return False
        elif request.method in ['PUT', 'PATCH']:
            return request.user and request.user.is_authenticated
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in ['PUT', 'PATCH']:
            return obj.user == request.user
        return False