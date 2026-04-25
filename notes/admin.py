from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display  = ('title', 'user', 'tag', 'is_pinned', 'document', 'updated_at')
    list_filter   = ('is_pinned', 'tag_color', 'user')
    search_fields = ('title', 'content', 'tag')
    readonly_fields = ('created_at', 'updated_at')
