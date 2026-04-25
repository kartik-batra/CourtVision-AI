from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('judge', 'Judge'),
        ('lawyer', 'Lawyer'),
        ('clerk', 'Court Clerk'),
        ('researcher', 'Legal Researcher'),
        ('admin', 'Administrator'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='researcher')
    bar_number = models.CharField(max_length=50, blank=True, null=True)
    court_affiliation = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('ta', 'Tamil'),
    ]
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_role_display()}"
