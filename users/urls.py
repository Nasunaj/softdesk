""" Urls routing for the users app.

This module defines Urls for the users app using DRF's DefaultRouter.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet

# Create a router and record Viewset
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

# Define application urls
urlpatterns = [
    path('', include(router.urls)),
]