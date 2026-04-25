from django.db import models
from django.contrib.auth.models import User
import os
import hashlib

def document_upload_path(instance, filename):
    return f'documents/{instance.uploaded_by.id}/{filename}'


class Document(models.Model):
    DOCUMENT_TYPES = [
        ('judgment', 'Court Judgment'),
        ('petition', 'Petition'),
        ('contract', 'Commercial Contract'),
        ('statute', 'Statute/Legislation'),
        ('brief', 'Legal Brief'),
        ('order', 'Court Order'),
        ('evidence', 'Evidence Document'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Processing Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    COURT_NAMES = [
        ("delhi high court", 'Delhi High Court'),
        ("bombay high court", 'Bombay High Court'),
        ("culcutta high court", 'Culcutta High Court'),
        ("madras high court", 'Madras High Court'),
        ('other', 'Other'),

    ]

    title = models.CharField(max_length=300)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, default='other')
    file = models.FileField(upload_to=document_upload_path)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    case_number = models.CharField(max_length=100, blank=True, null=True)
    court_name = models.CharField(max_length=200, choices=COURT_NAMES, default="other")
    filing_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    summary = models.TextField(blank=True, null=True)
    key_findings = models.TextField(blank=True, null=True)
    extracted_text = models.TextField(blank=True, null=True)
    page_count = models.IntegerField(default=0)
    file_size = models.BigIntegerField(default=0)
    vector_store_path = models.CharField(max_length=500, blank=True, null=True)
    word_count = models.IntegerField(default=0)
    chunk_count = models.IntegerField(default=0)
    summary_generated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_file_size_display(self):
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def filename(self):
        return os.path.basename(self.file.name)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Document"
        verbose_name_plural = "Documents"


class ResearchQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='queries')
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE,
        related_name='queries', null=True, blank=True
    )
    query_text = models.TextField()
    response_text = models.TextField(blank=True, null=True)
    sources = models.JSONField(default=list)
    response_length = models.IntegerField(default=0)   # char count of response
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query by {self.user.username}: {self.query_text[:60]}"

    def get_response_preview(self, chars=400):
        """Return a plain-text preview of the LLM response."""
        import re
        text = self.response_text or ''
        text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'\*{1,3}([^*\n]+)\*{1,3}', r'\1', text)
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s{2,}', ' ', text)
        return text.strip()[:chars] + "..."

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Research Query"
        verbose_name_plural = "Research Queries"

class TranslationCache(models.Model):
    """
    Permanent store of translated AI text.
    Key = SHA-256 of (source_text + target_language).
    Once translated, never re-translated — served from DB.
    """
    LANGUAGE_CHOICES = [
        ('hi', 'Hindi'),
        ('ta', 'Tamil'),
    ]

    content_hash    = models.CharField(max_length=64, db_index=True)
    source_text     = models.TextField()
    translated_text = models.TextField()
    target_language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES)
    char_count      = models.IntegerField(default=0)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('content_hash', 'target_language')
        verbose_name = "Translation Cache"
        verbose_name_plural = "Translation Cache"

    def __str__(self):
        return f"{self.target_language} | {self.content_hash[:12]}… ({self.char_count} chars)"

    @staticmethod
    def make_hash(text: str) -> str:
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    @classmethod
    def get_cached(cls, text: str, lang: str):
        """Return cached translation or None."""
        h = cls.make_hash(text)
        try:
            return cls.objects.get(content_hash=h, target_language=lang).translated_text
        except cls.DoesNotExist:
            return None

    @classmethod
    def store(cls, text: str, translated: str, lang: str) -> None:
        """Persist a translation permanently."""
        h = cls.make_hash(text)
        cls.objects.get_or_create(
            content_hash=h,
            target_language=lang,
            defaults={
                'source_text':     text,
                'translated_text': translated,
                'char_count':      len(text),
            }
        )
