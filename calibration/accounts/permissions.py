from rest_framework.permissions import BasePermission
from django.conf import settings

User = settings.AUTH_USER_MODEL


class AdminOrAuthenticatedUser(BasePermission):

    def has_permission(self, request, view):
        # Allow anyone to register
        if request.method == "POST":
            return True
        # Must be authenticated to view
        else:
            return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Any view method requires you to be the user
        return obj.id == request.user.id or request.user.is_staff
