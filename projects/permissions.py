"""Custom permissions for the SoftDesk API"""

from rest_framework import permissions
from projects.models import Project


# Class qui hérite de permissions.BasePermission-> classe de base pour créer
# des permissions personnalisées dans DRF.
class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors to edit their own ressources.
    - Read permissions (GET, HEAD, OPTIONS) are allowed to any authenticated
    user.
    - Write permissions (POST, PUT, PATCH, DELETE) are only allowed to the
    author.
    """

    def has_object_permission(self, request, view, obj):
        # Methode appelée pour vérifier si l'utilisateur a le droit d'accéder
        # à un objet spécifique (ex : une issue, un commentaire).
        if request.method in permissions.SAFE_METHODS:
            # Vérifie si la requête est une opération de lecture. Si oui, tout
            # utilisateur authentifié peut accèder à la ressource.
            return True
        # Vérifie si l'utilisateur actuel (request.user) est l'auteur de la
        # ressource (obj.author.user). Si oui, il peut modifier ou supprimer
        # la ressource.
        # return obj.author == request.user

        # Write permissions are only allowed to the author of the object
        # Gère le cas où obj.author est un Contributor (pour Issue, Comment,
        # etc.)
        if hasattr(obj, 'author') and hasattr(obj.author, 'user'):
            return obj.author.user == request.user
        # Gère le cas où obj.author est un User (pour Project, etc.)
        elif hasattr(obj, 'author'):
            return obj.author == request.user
        return False

class IsProjectAuthor(permissions.BasePermission):
    """
    Custom permission to only allow authors to edit the project author to add/
    remove contributors.
    - Only the author of the project can add or remove contributors..
    """

    def has_permission(self, request, view):
        # - Cette méthode est appelée avant que l'object ne soit récupéré ( pour
        # les  requêtes POST, PUT, PATCH, DELETE)
        # - Pour une requête POST /api/contributors/ (ajout d'un contributeur):
        # -- On récupère l'id du projet depuis request.data
        # -- On vérifie que l'utilisateur actuel est bien l'auteur du projet.
        # - Pour les autres méthodes (PUT, PATCH, DELETE) on laisse
        # has_object_permission gérer la vérification
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'POST':
            project_id = request.data.get('project')
            if not project_id:
                return False
            try:
                project = Project.objects.get(id=project_id)
                return project.author == request.user
            except Project.DoesNotExist:
                return False
        return True

    def has_object_permission(self, request, view, obj):
        # - Cette méthode est appelée après que l'objet ici un Contributor ait
        # été récuépré.
        # - On vérifie que l'utilisateur actuel est bien l'auteur du projet
        # associé au contributeur (obj.project.author)
        return obj.project.author == request.user