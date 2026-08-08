"""Serializers for the Issue and Comment models.

This module defines the serializers for the Issue and Comment models
to enable CRUD operations via the Django REST Framework API.
"""

from rest_framework import serializers
from issues.models import Issue, Comment
from projects.models import Contributor

class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model."""
    class Meta:
        """"""
        model = Comment
        fields = ['id', 'description', 'issue', 'author', 'uuid',
                  'created_time']
        read_only_fields = ['id', 'uuid', 'created_time', 'author']
        extra_kwargs = {
            'issue': {'required': True},
            'author': {'required': True},
        }

    def validate(self, data):
        """
        Validation personnalisée pour s'assurer que l'issue existe et que l'utilisateur est un contributeur.
        """
        issue = data.get('issue')
        if not issue:
            raise serializers.ValidationError(
                {"issue": "Ce champ est obligatoire."})

        # Vérifie que l'issue existe
        if not Issue.objects.filter(id=issue.id).exists():
            raise serializers.ValidationError(
                {"issue": "Cette issue n'existe pas."})

        return data

class IssueSerializer(serializers.ModelSerializer):
    """Serializer for the Issue model.

        This serializer includes the comments of the issue.
    """
    # Custom field to display issue comments.
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        """Define the model and fields to serialize."""
        model = Issue
        fields = ['id', 'title', 'description', 'status', 'priority', 'tag',
                  'project', 'assignee', 'author', 'created_time', 'comments']
        read_only_fields = ['id', 'created_time', 'author']
        extra_kwargs = {
            'project': {'required': True},
            'assignee': {'required': False},
        }

    def create(self, validated_data):
        """Create and return a new `Issue` instance, given the validated data.

        Automatically sets the author as the current user's contributor.
        """
        # Retrieve actual user
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            raise serializers.ValidationError('Doit être authentifié.')

        # Retrieve the user associated with the user and the project
        project = validated_data.get('project')
        user = request.user

        # Verify the user is a project contributor
        try:
            contributor = Contributor.objects.get(user=user, project=project)
        except Contributor.DoesNotExist:
            raise serializers.ValidationError("L'utilisateur n'est pas un "
                                              "contributeur du projet")
        # Remove `author` from validated_data to avoid conflicts
        validated_data.pop('author', None)

        # Create the issue with author (contributor)
        issue = Issue.objects.create(
            author=contributor,
            **validated_data
        )
        return issue

    def update(self, instance, validated_data):
        """
        Update and return an existing `Issue` instance, given the validated
        data.
        """

        # Retrieve the current user
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            raise serializers.ValidationError('Doit être authentifié.')

        user = request.user

        # Check that user is the author of the issue
        if instance.author.user != user:
            raise serializers.ValidationError("Seul l'auteur de l'issue peut "
                                              "la modifier.")
        # Update allowed fields
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description',
                                                  instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.tag = validated_data.get('tag', instance.tag)
        instance.assignee = validated_data.get('assignee', instance.assignee)
        instance.save()
        return instance

    def delete(self, instance):
        """Delete an existing `Issue` instance."""
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            raise serializers.ValidationError("Doit être authentifié.")

        user = request.user
        # Check that user is the author of the issue
        if instance.author.user != user:
            raise serializers.ValidationError("Seul l'auteur de l'issue peut la"
                                              "supprimer.")
        instance.delete()