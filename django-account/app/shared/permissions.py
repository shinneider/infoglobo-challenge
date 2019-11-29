from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthenticated(BasePermission):
    # message = 'No authenticated.'

    def has_permission(self, request, view):
        return request.headers.get('auth', None) == "true"


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.headers.get('auth', None) == "true"
        else:
            return True


class AllowAny(BasePermission):
    def has_permission(self, request, view):
        return True
