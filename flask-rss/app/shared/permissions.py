from flask import request as Request
from flask_restful import Resource

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsAuthenticated:
    # message = 'No authenticated.'
    @classmethod
    def has_permission(self, request, view):
        return request.headers.get('auth', None) == "true"


class IsAuthenticatedOrReadOnly:
    @classmethod
    def has_permission(self, request, view):
        if request.method not in SAFE_METHODS:
            return request.headers.get('auth', None) == "true"
        else:
            return True


class AllowAny:
    @classmethod
    def has_permission(self, request, view):
        return True


def Auth(cls):
    """
        This is a decorator to user Auth System

        decore the class usign this, add `permission_classes` in a class and 
        to be happy :)
        Ex:
            @Auth
            class XYZ:
                permission_classes = AllowAny  # all user have access
                ...
    """
    class NewCls(Resource):
        def base_auth(self, method, *args, **kwargs):
            if not cls.permission_classes.has_permission(request=Request, view=None):
                return {"error": "Authentication is required"}, 401

            method = getattr(cls, method, None)
            
            if method:
                return method(self, *args, **kwargs)
            
            return ({"message": "The method is not allowed for the requested URL."}, 405)

        def get(self, *args, **kwargs):
            return self.base_auth('get', *args, **kwargs)
        
        def post(self, *args, **kwargs):
            return self.base_auth('post', *args, **kwargs)
        
        def put(self, *args, **kwargs):
            return self.base_auth('put', *args, **kwargs)
        
        def patch(self, *args, **kwargs):
            return self.base_auth('patch', *args, **kwargs)
        
        def delete(self, *args, **kwargs):
            return self.base_auth('delete', *args, **kwargs)

    return NewCls