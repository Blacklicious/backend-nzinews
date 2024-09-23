from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Article(models.Model):
    category = models.CharField(max_length=255)
    title = models.JSONField(null=True)  # Store title in multiple languages as a dictionary
    content_introduction = models.JSONField(null=True)  # Store content intro in multiple languages as a dictionary
    content = models.JSONField(null=True)  # Store content in multiple languages as a dictionary
    content_conclusion = models.JSONField(null=True)  # Store content outro in multiple languages as a dictionary
    updated_at = models.DateTimeField(auto_now=True)
    tags =  models.JSONField(null=True)  # Store content outro in multiple languages as a dictionary
    total_views = models.IntegerField(default=0)
    total_likes = models.IntegerField(default=0)
    total_dislikes = models.IntegerField(default=0)
    total_saves = models.IntegerField(default=0)
    total_shares = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)
    total_reports = models.IntegerField(default=0)
    platform = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_from = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, default='draft')

    def __str__(self):
        # Attempt to return the title in English if available
        if isinstance(self.title, dict):
            return self.title.get('fr-FR', list(self.title.values())[0])  # Fallback to any available title if 'en' is not available
        return str(self.id)  # Fallback to converting title to string if it's not a dict
    
def article_image_upload_path(instance, filename):
    # Use slugify to make the category and title URL-safe
    category_slug = slugify(instance.article.category)
    # Create the dynamic path including the category and article title
    return f'images/news/articles/{category_slug}/{filename}'

class ArticleImage(models.Model):
    category = models.CharField(max_length=255)  # e.g. 'thumbnail', 'illustration'
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images', blank=True, null=True)
    image = models.ImageField(upload_to=article_image_upload_path,)  # Dynamically use the article category in path
    caption = models.CharField(max_length=255, blank=True)
    note = models.TextField(blank=True)
    tags = models.CharField(max_length=150, blank=True)  # e.g. 'p-1','a-0001'
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='active')

    def __str__(self):
        # Attempt to return the title in English if available
        return f"IMG-{self.article}-{self.id}"  # Fallback to converting title to string if it's not a dict

def article_audio_upload_path(instance, filename):
    # Use slugify to make the category and title URL-safe
    category_slug = slugify(instance.article.category)
    # Create the dynamic path including the category and article title
    return f'audios/news/articles/{category_slug}/{filename}'

class ArticleAudio(models.Model):
    category = models.CharField(max_length=255)  # e.g. 'thumbnail', 'illustration'
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='audios', blank=True, null=True)
    language = models.CharField(max_length=20, default='en')
    audio = models.FileField(upload_to=article_audio_upload_path,)  # Dynamically use the article category in path
    caption = models.CharField(max_length=255, blank=True)
    note = models.TextField(blank=True)
    tags = models.CharField(max_length=150, blank=True)  # e.g. 'p-1','a-0001'
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='active')

    def __str__(self):
        # Attempt to return the title in English if available
        return f"AUD-{self.article}-{self.id}"  # Fallback to converting title to string if it's not a dict

