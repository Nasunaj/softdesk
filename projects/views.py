"""Views for the Project and Contributor models.

This module defines the views for the Project and Contributor models
to handle CRUD operations via the Django REST Framework API.
"""
from rest_framework import viewsets, permissions
from projects.models import Project, Contributor
from projects.permissions import IsAuthorOrReadOnly, IsProjectAuthor
from projects.serializers import ProjectSerializer, ContributorSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    """Viewset for the Project model.

    This ViewSet provides CRUD operations for projects.
    Only authenticated users can create projects.
    """

    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        """Return only the Project where the user is a contributor."""
        user = self.request.user
        # Retrieves the projects where the user is the contributor.
        return Project.objects.filter(contributors__user=user)

    def perform_create(self, serializer):
        """Automatically set the author as the current user."""
        serializer.save(author=self.request.user)

class ContributorViewSet(viewsets.ModelViewSet):
    """ViewSet for the Contributor model.

    This ViewSet provides CRUD operations for contributors.
    Only the project author can add/remove contributors.
    """
    serializer_class = ContributorSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        # Seuls les auteurs du projet peuvent gérer les contributeurs
        IsProjectAuthor
    ]

    def get_queryset(self):
        """Return only the contributors for projects where the user is the
        author.
        """
        user = self.request.user
        return Contributor.objects.filter(project__author=user)

    def perform_create(self, serializer):
        """Automatically set the project and user for the contributor."""
        project = serializer.validated_data.get('project')
        # Verify the current user is the project author
        if project.author != self.request.user:
            raise permissions.PermissionDenied(
                "Seul l'auteur du projet peut ajouter des contributeurs.")
        serializer.save()