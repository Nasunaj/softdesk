"""Serializer for the Project and Contributor models.

This module defines the serializers for the Project and Contributor models
to enable CRUD operations via the Django REST Framework API.
"""

from rest_framework import serializers
from projects.models import Project, Contributor

class ContributorSerializer(serializers.ModelSerializer):
    """Serializer for the Contributor model."""
    class Meta:
        """Define the model and fields to serialize."""
        model = Contributor
        fields = ['id', 'user', 'project', 'role', 'created_time']
        read_only_fields = ['id', 'created_time']
        extra_kwargs = {
            'user': {'required': True},
            'project': {'required': True},
        }

class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for the Project model.

    This serializer includes the contributors of the project."""

    # Champ personnalisé pour afficher les contributeurs du projet
    contributors = ContributorSerializer(many=True, read_only=True)

    class Meta:
        """Define the model and fields to serialize."""
        model = Project
        fields = ['id', 'name', 'description', 'type', 'author',
                  'created_time', 'contributors']
        read_only_fields = ['id', 'created_time', 'author']
        extra_kwargs = {}

    def create(self, validated_data):
        """Create and return a new Project instance, given the validated data.

        Automatically adds the author as a Contributor with role AUTHOR.
        """
        # Retrieves the current user (project author)
        author = self.context['request'].user

        # Suppression `author` of validated_data if it's present
        # (bien qu'il soit read_only)
        validated_data.pop('author', None)

        # Create the project
        projet = Project.objects.create(
            author=author,
            **validated_data
        )

        # Add author as contributor with the AUTHOR role
        Contributor.objects.create(
            user=author,
            project=projet,
            role='AUTHOR',
        )
        return projet
