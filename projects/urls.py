"""URL routing for the projects app.

This module defines the URLs for the projects app using DRF's DefaultRouter.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from projects.views import ProjectViewSet, ContributorViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'contributors', ContributorViewSet,
                basename='contributor')

# Define the URLs of the application
urlpatterns = [
    path('', include(router.urls)),
]
