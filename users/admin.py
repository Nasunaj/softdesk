"""Admin interface configuration module for the User model.

This module customizes the display and filtering of users in the Django admin
panel for this application
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


class CustomUserAdmin(UserAdmin):
    """Custom class to manage the display of the User model in Django admin.

    This class extends UserAdmin to:
    - display the username, email, age, 'can_be_contacted',
    'can_data_be_shared'
    - Allow filtering user by 'can_be_contacted', 'can_data_be_shared'
    - Include RGPD fields in the creation and modification forms
    """

    # Champs affichés dans la liste des utilisateurs
    list_display = ('username', 'email', 'age', 'can_be_contacted',
                    'can_data_be_shared')

    # Champs pour filtrer les utilisateurs
    list_filter = ('can_be_contacted', 'can_data_be_shared')

    # Champs à inclure dans le formulaire de modification
    fieldsets = UserAdmin.fieldsets + (
        ('Informations RGPD', {
            'fields': ('age', 'can_be_contacted', 'can_data_be_shared'),
        }),
    )

    # Champs à inclure dans le formulaire de création
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'age',
                       'can_be_contacted', 'can_data_be_shared'),
        }),
    )


# Enregistre le modèle User avec la classe personnalisée
admin.site.register(User, CustomUserAdmin)
