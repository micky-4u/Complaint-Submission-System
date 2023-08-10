from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

# User models that includes employee and employers


class User(AbstractUser):
    is_email_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    # log in with email instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Issues(models.Model):
    issue_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(max_length=200)
    room_number = models.PositiveIntegerField(default=0000)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title
