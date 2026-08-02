"""Serializers for the User model.

This module defines the serializers for the User model to enable CRUD operation
via the django REST framework API.
"""

from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model.

    This serializer handles:
    - Serialization : convert User instance to JSON
    - Deserialization : convert JSON to User instance
    - Validation : Ensure data meets requirements (e.g., age >= 15)"""

    class Meta:
        """Define the model and fields to serialize."""

        model = User
        # Liste des champs à inclure dans la sérialisation
        fields = ['id', 'username', 'email', 'age', 'can_be_contacted',
                  'can_data_be_shared','password']
        # password : nécessaire pour la création/modification

        # Champs en lecture seule (ne peuvent pas être modifiés via l'API)
        read_only_fields = ['id']

        # Le mot de passe ne sera jamais retourné en JSON
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create and return a new `User` instance, given the validated data.

        This method is called when a POST request is made to create a new
        User.
        """
        # On extrait le mot de passe des données validées (.pop  supprime une
        # clé et retourne sa valeur de la clé)
        password = validated_data.pop('password', None)

        # On créé l'utilisateur avec les données restantes
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """Update and return an existing `User` instance, given the validated
        data.
        This method is called when a PUT/PATCH request is made to update a
        User.
        """
        # On extrait le mot de passe des données validées
        password = validated_data.pop('password', None)

        # on met à jour les champs de l'utilisateur
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
