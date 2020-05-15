from django.db import models
from apps.Authentication.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=65)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Post(models.Model):
    owner = models.ForeignKey(User, related_name='user_post', on_delete=models.CASCADE, )
    category = models.ForeignKey(Category, related_name='user_posts', on_delete=models.CASCADE)
    content = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    def __str__(self):
        return self.name
