from django.db import models
from django.contrib.auth.models import User

class Magazine(models.Model):
    category = models.CharField(max_length=255)
    title = models.CharField(max_length=255, unique=True)  # Title must be unique across all records
    thumbnail = models.ImageField(upload_to='images/news/magazines/thumbnails/', blank=True)
    content = models.FileField(upload_to='files/news/magazines/', blank=True)
    link = models.URLField(blank=True)
    description = models.TextField(blank=True)
    release_date = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=20, default='en')
    total_views = models.IntegerField(default=0)
    total_likes = models.IntegerField(default=0)
    total_dislikes = models.IntegerField(default=0)
    total_saves = models.IntegerField(default=0)
    total_shares = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)
    total_reports = models.IntegerField(default=0)
    publisher = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    tags = models.CharField(max_length=255,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_from = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, default='draft')

    def __str__(self):
        return f"{self.title}"