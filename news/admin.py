
from django.contrib import admin
from .models import Article, ArticleImage, ArticleAudio, Magazine, Podcast, Video, Job, Review
# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ( 'get_title', 'created_by', 'platform', 'status', 'created_at', 'updated_at', 'total_views', 'total_likes', 'total_dislikes')
    def get_title(self, obj):
        # Attempt to return the title in English ('en') if available
        if isinstance(obj.title, dict):
            return obj.title.get('en', list(obj.title.values())[0])  # Fallback to any available title if 'en' is not available
        return str(obj.title)  # Fallback to converting title to string if it's not a dict
    get_title.short_description = 'Title'  # Set column header in the admin panel

@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ('nzid', 'category', 'status', 'created_by', 'created_at', 'status')
    def nzid(self, obj):
        return f'IMG-{obj.article.id}-{obj.id}'  # Fallback to converting title to string if it's not a dict

@admin.register(ArticleAudio)
class ArticleAudioAdmin(admin.ModelAdmin):
    list_display = ('nzid', 'category', 'language', 'created_by', 'created_at', 'status')
    def nzid(self, obj):
        return f'AUD-{obj.article.id}-{obj.id}'  # Fallback to converting title to string if it's not a dict

@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','publisher', 'created_by', 'release_date', )

@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','publisher', 'created_by', 'release_date', )

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','publisher', 'created_by', 'release_date', )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'review_type', 'content_type', 'content_id', 'created_at', 'status')


admin.site.register(Job)
