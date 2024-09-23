from django.db import models
from django.contrib.auth.models import User

# Create your models here.
   
class Employee(models.Model):
    USER_ROLES = (
        ('manager', 'Manager'),
        ('supervisor','Supervisor'),
        ('moderator', 'Moderator'),
        ('creator', 'Creator'),
        ('full-time', 'Full-Time'),
        ('temporary', 'Temporary'),
        ('job_hunter', 'Job Hunter'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=USER_ROLES, default='job_hunter')
    business = models.ForeignKey('Business', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='images/profiles/professionals/', blank=True)  # Use the default storage backend (Google Cloud Storage)
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='files/professionals/resumes/', blank=True)  # Use the default storage backend (Google Cloud Storage)
    #--------------------------------------------------------------------------------
    job_nzid = models.IntegerField( blank=True)
    job_department = models.CharField(max_length=255, blank=True)
    job_title = models.CharField(max_length=255, blank=True)
    job_email = models.EmailField(max_length=255, blank=True)
    job_phone = models.CharField(max_length=15, blank=True)
    #--------------------------------------------------------------------------------
    tags = models.CharField(max_length=150, blank=True)
    note = models.TextField(blank=True)
    #--------------------------------------------------------------------------------
    platform = models.CharField(max_length=50, blank=True) # e.g. 'T-MAK'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_from = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

