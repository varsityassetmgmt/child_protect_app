from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('parent', 'Parent'),
        ('child', 'Child'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.user.username


class RestrictedURL(models.Model):
    url = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    min_age = models.IntegerField(default=0)
    max_age = models.IntegerField(default=17)

    def __str__(self):
        return f"{self.url} ({self.min_age}-{self.max_age})"