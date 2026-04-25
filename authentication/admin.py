from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'court_affiliation', 'created_at')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email', 'court_affiliation')
