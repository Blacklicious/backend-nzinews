from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .article import Article
from .magazine import Magazine
from .podcast import Podcast
from .video import Video

class Review(models.Model):
    REVIEW_TYPES = [
        ('viewed', 'Viewed'),
        ('like', 'Like'),
        ('dislike', 'Dislike'),
        ('comment', 'Comment'),
        ('saved', 'Saved'),
        ('shared', 'Shared'),
        ('report', 'Report'),
    ]
    review_type = models.CharField(max_length=10, choices=REVIEW_TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=20)  # e.g. "article", "magazine", "podcast", "video"
    content_id = models.IntegerField()
    reviews = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='active')

    def __str__(self):
        return f"{self.user.username} - {self.review_type} - {self.content_type} ({self.content_id})"

    def update_totals(self):
        content_model = None
        if self.content_type == "article":
            content_model = Article
        elif self.content_type == "magazine":
            content_model = Magazine
        elif self.content_type == "podcast":
            content_model = Podcast
        elif self.content_type == "video":
            content_model = Video
        
        if content_model:
            content = content_model.objects.get(id=self.content_id)
            if self.review_type == 'viewed':
                content.total_views += 1
            elif self.review_type == 'like':
                content.total_likes += 1
            elif self.review_type == 'dislike':
                content.total_dislikes += 1
            elif self.review_type == 'saved':
                content.total_saves += 1
            elif self.review_type == 'shared':
                content.total_shares += 1
            elif self.review_type == 'comment':
                content.total_comments += 1
            elif self.review_type == 'report':
                content.total_reports += 1
            content.save()

@receiver(post_save, sender=Review)
def update_content_totals_on_save(sender, instance, created, **kwargs):
    instance.update_totals()

@receiver(post_delete, sender=Review)
def update_content_totals_on_delete(sender, instance, **kwargs):
    content_model = None
    if instance.content_type == "article":
        content_model = Article
    elif instance.content_type == "magazine":
        content_model = Magazine
    elif instance.content_type == "podcast":
        content_model = Podcast
    elif instance.content_type == "video":
        content_model = Video
    
    if content_model:
        content = content_model.objects.get(id=instance.content_id)
        if instance.review_type == 'viewed':
            content.total_views -= 1
        elif instance.review_type == 'like':
            content.total_likes -= 1
        elif instance.review_type == 'dislike':
            content.total_dislikes -= 1
        elif instance.review_type == 'saved':
            content.total_saves -= 1
        elif instance.review_type == 'shared':
            content.total_shares -= 1
        elif instance.review_type == 'comment':
            content.total_comments -= 1
        elif instance.review_type == 'report':
            content.total_reports -= 1
        content.save()