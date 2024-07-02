from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.
class User(AbstractUser):

    email = models.EmailField(unique=True, blank=False, null=False, error_messages = {
        "unique": "A user with that email already exists.",
    })


class Chapter(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="UserChapters"
    )
    OCRText = models.TextField()
    title = models.CharField(max_length=200)
    summary = models.TextField()
    notes = models.JSONField(default=list)
    flashcards = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    last_opened = models.DateTimeField(null=True, blank=True)

    def update_last_opened(self):
        self.last_opened = timezone.now()
        self.save()
