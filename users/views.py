"""Vieuw for the model.

This module defines the views for the User model to handle CRUD operation via
the Django REST Framework. API
"""

from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from users.serializers import UserSerializer, SignupSerializer
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


class SignupView(generics.CreateAPIView):
    """
    View for user signup.
    - Allows any user (authentificated or not) to create an account.
    - Validates that password1 and password2 match.
    """

    serializer_class = SignupSerializer
    # Autorise l'accès à tous (même non authentifiés)
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        """Override the create method to return a success message."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # create user
        user = serializer.save()
        # return a custom response
        return Response({
            'message': 'Compte créé avec succès.',
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
        }, status=status.HTTP_201_CREATED
        )
