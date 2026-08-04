"""Models for the Issue and Comment.

This module defines the Issue and Comment models for the SoftDesk application.
"""
from django.db import models
from projects.models import Project, Contributor

class Issue (models.Model):
    """Model representing an Issue(task, bug or feature) in a project.
    Attributes:
        title (str): The title of the issue.
        description (str): The description of the issue.
        status (str): The status of the issue (TO_DO, IN_PROGRESS, FINISHED).
        priority (str): The priority of the issue (LOW, MEDIUM, HIGH).
        tag (str): The tag of the issue (BUG, FEATURE, TASK).
        project (Project): The project to which the user contributes.
        assignee (Contributor): The contributor assigned to the issue.
        author (Contributor): The contributor who created the issue.
        created_time (datetime): When the issue was created.
    """
    STATUS_CHOICES = [
        ('TO_DO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('FINISHED', 'Finished'),
    ]
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    TAG_CHOICES = [
        ('BUG', 'Bug'),
        ('FEATURE', 'Feature'),
        ('TASK', 'Task'),
    ]
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=8192, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=11,
                              default='TO_DO')
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=6,
                                default='MEDIUM')
    tag = models.CharField(choices=TAG_CHOICES, max_length=7, default='TASK')
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name='issues')
    assignee = models.ForeignKey(Contributor,
                                 # If the Contributor is deleted, the assignee
                                 # becomes NULL.
                                 on_delete=models.SET_NULL,
                                 # Allows NULL values in the database
                                 null=True,
                                 # Allows empty values in Django forms
                                 blank=True,
                                 related_name='assigned_issues')
    author = models.ForeignKey(Contributor, on_delete=models.CASCADE,
                               related_name='created_issues')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the Issue model."""
        return f"{self.title} ({self.status}) in {self.project.name}"

class Comment (models.Model):
    """Model  representing a comment on an issue.

    Attributes:
        description (str): The description of the comment.
        issue (Issue): The issue to which the comment belongs.
        author (Contributor): The contributor who created the comment.
        uuid (str): a unique identifier for the comment.
        created_time (datetime): When the comment was created.
    """
    import uuid
    description = models.TextField(max_length=8192)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE,
                              related_name='comments')
    author = models.ForeignKey(Contributor, on_delete=models.CASCADE,
                               related_name='created_comments')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        """Return a string representation of the Issue model."""
        return f"Comment by {self.author.user.username} on {self.issue.title}"
