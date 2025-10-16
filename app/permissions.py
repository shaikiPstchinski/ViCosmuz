from rest_framework import permissions

class isAstronomer(permissions.BasePermission):

    def hasPermission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.type == 'Astronomer'