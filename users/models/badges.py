from django.db import models
from django.contrib.auth.models import User
from .businesses import Business

class Badge(models.Model):
    type = models.CharField(max_length=100, blank=True, null=True)  # e.g., 'Achievement', 'Certification'
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user_badges')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='business_badges')
    image = models.JSONField(blank=True)
    platform = models.CharField(max_length=50) # e.g. 'TMAK'
    created_by = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='created_badges')  # The user who created the badge
    created_from = models.CharField(max_length=50, blank=True)
    issued_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name
