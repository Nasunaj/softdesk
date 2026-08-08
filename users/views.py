"""Vieuw for the model.

This module defines the views for the User model to handle CRUD operation via
the Django REST Framework. API
"""
from django.shortcuts import render
from rest_framework import viewsets, permissions
from users.models import User
from users.serializers import UserSerializer
from users.permissions import IsAdminOrSelf

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """Viewset for the User model.

    The viewset provides the following actions:
    - list: GET/users/(list all users)
    - retrieve: GET/users/{id}/(retrieve a single user)
    - update: PUT/users/{id}/(update a user)
    - partial_update: PATCH/users/{id}/(partial update a user)
    - destroy: DELETE/users/{id}/(delete a user)
    """
    # specifies the model to use
    queryset = User.objects.all()

    # Specifies the serializer to use
    serializer_class = UserSerializer

    # Specifies the permission (only admin can list users)
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = [
        # L'utilisateur doit être authentifié
        permissions.IsAuthenticated,
        # Applique la permission personnalisée
        IsAdminOrSelf,
    ]
