"""URL routing for the issues app.

This module defines the URLs for the issues app using DRF's DefaultRouter.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from issues.views import IssueViewSet, CommentViewSet

# Create a router and save the ViewSets
router = DefaultRouter()
router.register(r'issues', IssueViewSet, basename='issue')
router.register(r'comments', CommentViewSet, basename='comment')

# Définit les URLs de l'application
urlpatterns = [
    path('', include(router.urls)),
]
