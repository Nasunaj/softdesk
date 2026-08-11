"""Models for the Project and Contributor.

This module defines the Project and Contributor models for the softdesk
application.
"""
from django.db import models
from users.models import User


class Project(models.Model):
    """ model representing a project in softdesk.

    Attributes:
        name (str): the name of the project.
        description (str): the description of the project.
        type (str): the type of the project (e.g., back-end, front-end, iOS,
        Android).
        author (User): the user who created the project (autmatically a
        contributor).
        created_time (datetime): when the project was created.
    """
    PROJECT_TYPES = [
        ('BACKEND', 'Back-end'),
        ('FRONTEND', 'Front-end'),
        ('IOS', 'ios'),
        ('ANDROID', 'android'),
    ]
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=8192, blank=True)
    type = models.CharField(max_length=10, choices=PROJECT_TYPES)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='projects_created')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the project."""
        return f"{self.name} ({self.type})"


class Contributor(models.Model):
    """Model representing a contributor to a project.

    Attributes:
        user (User): The user who is a contributor.
        project (Project): The project to which the user contributes.
        role (str): The role of the contributor (e.g., author, member).
    """
    ROLE = [
        ('AUTHOR', 'Author'),
        ('MEMBER', 'Member'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='contributions')
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name='contributors')
    role = models.CharField(max_length=10, choices=ROLE, default='MEMBER')
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for the Contributor model."""
        # A user can be a contributor only once per project.
        unique_together = ('user', 'project')

    def __str__(self):
        """Return a string representation of the project."""
        return f"{self.user.username} ({self.role}) in {self.project.name}"
