"""Views for the Issue and Comment models.

This module defines the views for the Issue and Comment models to handle
CRUD operations via the Django REST Framework API.
"""

from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from issues.models import Issue, Comment
from issues.serializers import IssueSerializer, CommentSerializer
from projects.models import Contributor
from projects.permissions import IsAuthorOrReadOnly

class IssueViewSet(viewsets.ModelViewSet):
    """ViewSet for the Issue model.

    This ViewSet provides CRUD operations for issues.
    Only authenticated users who are contributors to the project can create or modify issues.
    """
    serializer_class = IssueSerializer
    permission_classes = [
        # L'utilisateur doit être authentifié
        permissions.IsAuthenticated,
        # Applique la permission personnalisée
        IsAuthorOrReadOnly
        ]

    def get_queryset(self):
        """Return only the issues for projects where the user is a contributor.
        """
        user = self.request.user
        # Retrieves issues from projects where the user is a contributor
        return Issue.objects.filter(project__contributors__user=user)

    def perform_create(self, serializer):
        """Automatically set the author as the current user's contributor for
        the project.
        """
        # The serializer already handles the author via its create method.
        serializer.save()

    def perform_update(self, serializer):
        """Ensure only the author or project contributors can update the issue.
        """
        issue = serializer.instance
        user = self.request.user
        # Checks that the user is the author of the issue or a project
        # contributor
        if issue.author.user != user and not Contributor.objects.filter(
                user=user, project=issue.project
        ).exists():
            raise PermissionDenied(
                "Seul l'auteur de l'issue ou un contributeur du projet peut la modifier."
            )
        serializer.save()

    def perform_destroy(self, instance):
        """Ensure only the author can delete the issue."""
        user = self.request.user
        if instance.author.user != user:
            raise PermissionDenied(
                "Seul l'auteur de l'issue peut la supprimer.")
        instance.delete()

class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for the Comment model.
    This ViewSet provides CRUD operations for comments.
    Only authenticated users who are contributors to the project can create or
    modify issues.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        """Return only the comments for projects where the user is a
        contributor.
        """
        user = self.request.user
        return Comment.objects.filter(issue__project__contributors__user=user)

    def perform_create(self, serializer):
        """Automatically set the author as the current user's contributor for
        the issue's project.
        """
        issue = serializer.validated_data.get("issue")
        user = self.request.user

        try:
            contributor = Contributor.objects.get(user=user,
                                                  project=issue.project)
        except Contributor.DoesNotExist:
            raise PermissionDenied(  # <-- Utilise PermissionDenied
                "L'utilisateur n'est pas un contributeur du projet de cette "
                "issue."
            )
        serializer.save(author=contributor)

    def perform_update(self, serializer):
        """Ensure only the author can update the comment."""
        comment = serializer.instance
        user = self.request.user
        if comment.author.user != user:
            raise PermissionDenied("Seul l'auteur du commentaire peut le modifier.")
        serializer.save()

    def perform_destroy(self, instance):
        """Ensure only the author can delete the comment."""
        user = self.request.user
        if instance.author.user != user:
            raise PermissionDenied("Seul l'auteur du commentaire peut le supprimer.")
        instance.delete()
