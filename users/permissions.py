"""Custom permissions for the user model."""

from rest_framework import permissions


class IsAdminOrSelf(permissions.BasePermission):
    """
    Custom permission to only allow :
    - Admins to perform any action
    - Users to read or update their awn profile.
    """

    def has_permission(self, request, view):
        # Pour une requête GET /api/users/ (liste de tous les utilisateurs,
        # seul un admin (is_staff=True) peut y accèder.
        if request.method == 'GET' and view.action == 'list':
            return request.user.is_staff
        # Pour les autres actions (GET /api/users/{id}/, PUT, etc.) on laisse
        # has_object_permission gérer la vérification.
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Lecture (GET, HEAD, OPTIONS): un utilisateur peut lire ses
            # propres données ou un admin peut tout lire.
            return request.user == obj or request.user.is_staff
        # Ecrire (PUT, PATCH, DELETE) : un utilisateur peut modifier ses
        # propres données ou un admin peut tout modifier.
        return request.user == obj or request.user.is_staff
