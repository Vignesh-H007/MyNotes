from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Note(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    title = models.CharField(max_length = 200)
    content = models.TextField()
    subject_key = models.CharField(max_length=100, blank=True, null=True)
    is_favourite = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    attachment_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)