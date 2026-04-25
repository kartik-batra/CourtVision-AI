from django.contrib import admin
from .models import Document, ResearchQuery, TranslationCache

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_type', 'uploaded_by', 'status', 'created_at')
    list_filter = ('document_type', 'status')
    search_fields = ('title', 'case_number')
    readonly_fields = ('created_at', 'updated_at', 'extracted_text', 'summary')

@admin.register(ResearchQuery)
class ResearchQueryAdmin(admin.ModelAdmin):
    list_display = ('user', 'query_text', 'created_at')
    list_filter = ('user',)

@admin.register(TranslationCache)
class TranslationCaheAdmin(admin.ModelAdmin):
    list_display  = ('content_hash_short', 'target_language', 'char_count', 'created_at')
    list_filter   = ('target_language',)
    readonly_fields = ('content_hash', 'source_text', 'translated_text', 'char_count', 'created_at')
    search_fields = ('content_hash',)

    def content_hash_short(self, obj):
        return obj.content_hash[:16] + '…'
    content_hash_short.short_description = 'Hash'
