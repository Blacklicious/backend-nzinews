from rest_framework import routers
from django.urls import path, include

from .views.article import get_articles, get_articles_with_images, get_article, get_article_images, create_article, upload_article_image, delete_article 
from .views.articles.audio import create_article_audio, get_article_audios
from .views.magazine import get_magazines, get_magazine, create_magazine, update_magazine, delete_magazine
from .views.video import get_videos, get_video, create_video, update_video, delete_video
from .views.job import get_jobs, create_job, activate_job, deactivate_job, job_detail

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    # ----------------------------------------- Article URLs -----------------------------------------
    path('articles/api/', get_articles, name='get_articles'),  # URL endpoint for fetching articles
    path('articles-full/api/', get_articles_with_images, name='get_articles_with_images'),
    path('article/<int:pk>/api/', get_article, name='get_article'),
    path('article/api/', create_article, name='create-article'),  # URL endpoint for creating a new magazine
    path('article/<int:article_id>/images/api/', get_article_images, name='get_article_images'),
    path('articles/image/api/', upload_article_image, name='upload-article-image'),
    path('article/<int:article_id>/generate-audio/api/', create_article_audio, name='create_article_audio'),
    path('articles/audios/api/', get_article_audios, name='get_article_audios'),
    path('article/<int:pk>/delete/api/', delete_article, name='delete-article'),  # URL endpoint for deleting a magazine

    # ----------------------------------------- Magazine URLs -----------------------------------------
    path('magazines/api/', get_magazines, name='get-magazines'),  # URL endpoint for fetching magazines
    path('magazine/<int:pk>/api/', get_magazine, name='get-magazine'),  # URL endpoint for fetching a magazine
    path('magazine/api/', create_magazine, name='create-magazine'),  # URL endpoint for creating a new magazine
    path('magazine/<int:pk>/api/', update_magazine, name='update-magazine'),  # URL endpoint for updating a magazine
    path('magazine/<int:pk>/delete/api/', delete_magazine, name='delete-magazine'),  # URL endpoint for deleting a magazine
    # ----------------------------------------- Video URLs -----------------------------------------
    path('videos/api/', get_videos, name='get-videos'),  # URL endpoint for fetching videos
    path('video/<int:pk>/api/', get_video, name='get-video'),  # URL endpoint for fetching a video
    path('video/api/', create_video, name='create-video'),  # URL endpoint for creating a new video
    path('video/<int:pk>/api/', update_video, name='update-video'),  # URL endpoint for updating a video
    path('video/<int:pk>/delete/api/', delete_video, name='delete-video'),  # URL endpoint for deleting a video
    # ----------------------------------------- Audio URLs -----------------------------------------
    # path('audios/api/', get_audios, name='get-audios'),  # URL endpoint for fetching audios
    # path('audio/api/', create_audio, name='create-audio'),  # URL endpoint for creating a new audio
    # path('audio/<int:pk>/api/', update_audio, name='update-audio'),  # URL endpoint for updating an audio
    # path('audio/<int:pk>/delete/api/', delete_audio, name='delete-audio'),  # URL endpoint for deleting an audio
    # ----------------------------------------- Job URLs -----------------------------------------
    path('jobs/api/', get_jobs, name='get-jobs'),
    path('job/api/', create_job, name='create-job'),
    path('jobs/<int:pk>/api', job_detail, name='job-detail'),
    path('jobs/<int:pk>/api/activate/', activate_job, name='activate-job'),
    path('jobs/<int:pk>/api/deactivate/', deactivate_job, name='deactivate-job'),
]
