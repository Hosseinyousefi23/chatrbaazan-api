from rest_framework.permissions import BasePermission


class AllowAnyAnonymous(BasePermission):
    """
    Allow any access.
    This isn't strictly required, since you could use an empty
    permission_classes list, but it's useful because it makes the intention
    more explicit.
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return True
        return False
