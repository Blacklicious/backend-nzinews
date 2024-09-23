from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Member(models.Model):
    USER_ROLES = (
        ('member', 'Member'),
        ('staff', 'Staff'),
        ('creator', 'Creator'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=50, choices=USER_ROLES, default='member' )
    bio = models.TextField(blank=True)
    age = models.IntegerField(null=True, blank=True)  # New age field
    sex = models.CharField(max_length=50, blank=True)
    #--------------------------------------------------------------------------------
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField( blank=True)
    image = models.ImageField(upload_to='images/profiles/members/')  # Use the default storage backend (Google Cloud Storage)
    #--------------------------------------------------------------------------------
    language = models.CharField(max_length=50, blank=True)
    note = models.TextField(blank=True)
    #--------------------------------------------------------------------------------
    platform = models.CharField(max_length=50, blank=True) # e.g. 'T-MAK'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_from = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=50, blank=True, default='inactive')

    def __str__(self):
        return f"{self.user.username} Profile"

