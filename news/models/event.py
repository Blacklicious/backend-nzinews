from django.db import models
from django.contrib.auth.models import User  # Assuming you're using Django's built-in User model

# Event model representing an event
class Event(models.Model):
    title = models.CharField(max_length=255)  # Title of the event
    description = models.TextField()  # Detailed description of the event
    location = models.CharField(max_length=255)  # Location of the event
    start_date = models.DateTimeField()  # Start date and time of the event
    end_date = models.DateTimeField()  # End date and time of the event
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="organized_events")  # Event organizer (optional)
    event_type = models.CharField(max_length=50, choices=[('conference', 'Conference'), ('workshop', 'Workshop'), ('webinar', 'Webinar'), ('meetup', 'Meetup')])  # Type of event
    max_participants = models.IntegerField(blank=True, null=True)  # Optional max number of participants
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Price of the event (optional)
    tags = models.CharField(max_length=255, blank=True, null=True)  # Optional tags or keywords
    banner = models.ImageField(upload_to='images/events/banners/', blank=True, null=True)  # Image for the event banner
    website = models.URLField(blank=True, null=True)  # Optional URL for more information
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time the event was created
    updated_at = models.DateTimeField(auto_now=True)  # Date and time the event was last updated
    status = models.CharField(max_length=50, blank=True, null=True)  # Status of the event (e.g., active, inactive)

    def __str__(self):
        return self.title

# EventRegistration model representing a user's registration to an event
class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')  # Event the user is registering for
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who is registering
    registered_at = models.DateTimeField(auto_now_add=True)  # Date and time the user registered
    status = models.CharField(max_length=50, choices=[('registered', 'Registered'), ('canceled', 'Canceled'), ('attended', 'Attended')], default='registered')  # Registration status

    def __str__(self):
        return f'{self.user.username} - {self.event.title}'


# EventImage model representing images associated with an event
class EventImage(models.Model):
    category = models.CharField(max_length=50, blank=True, null=True)  # Optional category for the image
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')  # The event the image belongs to
    title = models.CharField(max_length=255, blank=True, null=True)  # Optional title for the image
    image = models.ImageField(upload_to='event_images/')  # The image file
    description = models.CharField(max_length=255, blank=True, null=True)  # Optional description of the image
    tags = models.CharField(max_length=255, blank=True, null=True)  # Optional tags or keywords
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Date the image was uploaded
    platform = models.CharField(max_length=50, blank=True, null=True)  # Platform where the image was uploaded
    status = models.CharField(max_length=50, blank=True, null=True)  # Status of the image (e.g., active, inactive)

    def __str__(self):
        return f"Image for {self.event.title}" 