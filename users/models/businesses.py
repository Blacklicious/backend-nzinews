from django.db import models
from django.contrib.auth.models import User

class Business(models.Model):
    industry = models.JSONField(blank=True, null=True) # e.g. 'Agriculture', 'Education', 'Health', 'Technology', etc
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    registration_date = models.DateTimeField(blank=True, null=True)
    license = models.CharField(max_length=250, blank=True)
    #--------------------------------------------------------------------------------
    logo = models.ImageField(upload_to='images/profiles/businesses/logos/', blank=True) 
    #--------------------------------------------------------------------------------
    email = models.EmailField(max_length=255, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    website = models.URLField(max_length=255, blank=True)
    social = models.JSONField(blank=True, null=True)
   #--------------------------------------------------------------------------------
    tags = models.CharField(max_length=150, blank=True)
    owners = models.ManyToManyField(User, blank=True, related_name='owned_businesses')
    managers = models.ManyToManyField(User, blank=True, related_name='managed_businesses')
    supervisors = models.ManyToManyField(User, blank=True, related_name='supervised_businesses')
    fulltime_employees = models.ManyToManyField(User, blank=True, related_name='fulltime_businesses')
    parttime_employees = models.ManyToManyField(User, blank=True, related_name='parttime_businesses')
    consultants = models.ManyToManyField(User, blank=True, related_name='consultant_businesses')
    interns = models.ManyToManyField(User, blank=True, related_name='interned_businesses')
   #--------------------------------------------------------------------------------
    platform = models.CharField(max_length=50) # e.g. 'TMAK'
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_businesses')
    created_from = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

# Model for multiple images for Business
class BusinessImage(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/profiles/businesses/', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.business.name}"

    