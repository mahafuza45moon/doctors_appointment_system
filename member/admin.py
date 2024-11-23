from django.contrib import admin
from .models import AppUser

@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'specialty', 'date_of_birth')
