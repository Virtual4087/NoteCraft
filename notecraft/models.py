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
    title = models.CharField(max_length=75, blank=False, null=False)
    summary = models.TextField()
    notes = models.JSONField(default=list)
    flashcards = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    last_opened = models.DateTimeField(null=True, blank=True)

    def update_last_opened(self):
        self.last_opened = timezone.now()
        self.save()

    def update_title(self, title):
        if title == "":
            raise ValueError("Title cannot be empty.")
        if len(title) > 75:
            raise ValueError("Title cannot be longer than 75 characters.")
        self.title = title
        self.save()