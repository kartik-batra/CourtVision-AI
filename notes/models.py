from django.db import models
from django.contrib.auth.models import User
from documents.models import Document


class Note(models.Model):
    TAG_COLORS = [
        ('gold',    '#c9a84c'),
        ('blue',    '#3498db'),
        ('green',   '#2ecc71'),
        ('red',     '#e74c3c'),
        ('purple',  '#9b59b6'),
        ('orange',  '#e67e22'),
    ]

    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    document   = models.ForeignKey(
        Document, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='notes'
    )
    title      = models.CharField(max_length=300)
    content    = models.TextField()
    tag        = models.CharField(max_length=50, blank=True, default='')
    tag_color  = models.CharField(max_length=10, choices=TAG_COLORS, default='gold')
    is_pinned  = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-updated_at']

    def __str__(self):
        return f"{self.user.username} — {self.title[:60]}"

    def content_preview(self, chars=180):
        return self.content[:chars] + ('…' if len(self.content) > chars else '')
