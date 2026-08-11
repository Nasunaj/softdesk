"""User model for the softdesk application.

This module defines the User model, which extends AbstractUser to add field for
RGPD.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class User(AbstractUser):
    """User model."""
    # Additional field for RGPD
    age = models.IntegerField(
        validators=[MinValueValidator(15)],
        help_text="L'utilisateur doit avoir au moins 15 ans pour s'inscrire.")
    can_be_contacted = models.BooleanField(
        default=False,
        help_text="Autorisez-vous à être contacté par d'autres utilisateurs?"
    )
    can_data_be_shared = models.BooleanField(
        default=False,
        help_text="Autorisez-vous le partage de vos données avec des tiers?"
    )

    def __str__(self):
        """Return username."""
        return self.username
