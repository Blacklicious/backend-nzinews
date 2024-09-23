from django.db import models
from django.contrib.auth.models import User  # Assuming you're using Django's built-in User model
from users.models import Business  # Import the Business model from the users app

# Job model representing a job posting
class Job(models.Model):
    title = models.CharField(max_length=255)  # Job title
    job_type = models.CharField(max_length=50, choices=[('full-time', 'Full-time'), ('part-time', 'Part-time'), ('contract', 'Contract')])  # Type of job
    description = models.TextField()  # Job description
    qualifications = models.TextField()  # Job qualifications or requirements
    location = models.CharField(max_length=255)  # Job location
    salary_range = models.CharField(max_length=100, blank=True, null=True)  # Salary range for the job
    company = models.ForeignKey(Business, on_delete=models.CASCADE)  # Reference to the company posting the job
    posted_date = models.DateTimeField(auto_now_add=True)  # Date the job was posted
    expiration_date = models.DateField(null=True, blank=True)  # Date after which the job is no longer available
    platform = models.CharField(max_length=50, blank=True) # e.g. 'T-MAK'
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # User who created the job posting
    status = models.CharField(max_length=50, blank=True)  # Status of the job posting (e.g., active, inactive

    def __str__(self):
        return self.title
