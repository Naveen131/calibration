from rest_framework.permissions import BasePermission
from django.conf import settings

User = settings.AUTH_USER_MODEL


class IsAdmin(BasePermission):

    def has_permission(self, request, view):

        print(request.user.is_active)
        return request.user and request.user.is_staff

# class IsOwnerOrAdmin(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_active or request.user.is_staff
