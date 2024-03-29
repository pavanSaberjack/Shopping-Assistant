from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit his profile"""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class PostOwnStatus(permissions.BasePermission):
    """Allow logged in users to edit their feed"""

    def has_object_permission(self, request, view, obj):
        """Check the user is trying to update their own status"""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id

class AddToYourList(permissions.BasePermission):
    """Allow logged in users to edit their feed"""

    def has_object_permission(self, request, view, obj):
        """Check the user is trying to update their own status"""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id
