# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from ..models import Article, ArticleImage, ArticleAudio
from ..serializers import ArticleSerializer, ArticleImageSerializer, ArticleAudioSerializer
from django.contrib.auth.models import User

from google.cloud import translate_v2 as translate
from django.http import JsonResponse
from rest_framework import status

from django.conf import settings

from django.contrib.auth.decorators import user_passes_test

# Check if the user is an manager or moderator
def is_manager_supervisor_moderator_fulltime_parttime_creator(user):
    return user.member.role in ['manager', 'supervisor', 'moderator', 'creator', 'full-time', 'part-time']

@user_passes_test(is_manager_supervisor_moderator_fulltime_parttime_creator)
def update_article(request, article_id):
    # Your logic to update the article goes here
    pass

# Initialize the translation client
translate_client = translate.Client(credentials=settings.GT_CREDENTIALS)
print('translate_client ---->',translate_client)


# API to create an article
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Authentication required
def create_article(request):
    data = request.data
    print('DATA REQUEST ---->',data)
    available_languages = ['en-GB', 'fr-FR', 'es-ES']  # Add the list of languages you support

    # Prepare the article fields for translation
    content_language = data.get('language', 'en-GB')
    title = data.get('title', {})
    
    # Check if the article with the same title (in 'en') already exists
    if content_language in title:
        print('title[content_language] ---->', title[content_language])
        title_to_search = title[content_language]
        # Use __has_key to check if the content_language exists in the title JSON field
        # Retrieve all articles and filter in Python
    existing_articles = Article.objects.all()

    # Filter in Python for the title match
    existing_article = None
    for article in existing_articles:
        if content_language in article.title and article.title[content_language] == title_to_search:
            existing_article = article
            break

    print('existing_article ---->', existing_article)

    if existing_article:
        print('existing_article ----> True')
        return Response({'error': 'An article with this title already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    # Proceed with further translation and processing
    content_introduction = data.get('content_introduction', {})
    content = data.get('content', {})
    content_conclusion = data.get('content_conclusion', {})

    # Function to detect language and ensure text is passed correctly
    def detect_language(text):
        if isinstance(text, str) and text.strip():
            result = translate_client.detect_language(text)
            return result.get('language', 'en-GB')
        return 'en'  # Default to English if detection fails or text is not a string

    # Function to translate text to target languages
    def translate_text(text, target_lang):
        if isinstance(text, str) and text.strip():
            result = translate_client.translate(text, target_language=target_lang)
            return result['translatedText']
        return text  # Return the original text if it's empty or invalid
    
    # For each field, detect language and translate missing ones
    for lang in available_languages:
        # Translate title
        if lang not in title:
            detected_language = detect_language(title.get(content_language, ''))
            title[lang] = translate_text(title.get(detected_language), lang)

        # Translate content introduction
        if lang not in content_introduction:
            detected_language = detect_language(content_introduction.get(content_language, ''))
            content_introduction[lang] = translate_text(content_introduction.get(detected_language), lang)

        # Translate content paragraphs
        if lang not in content:
            # Since paragraphs are a list of dictionaries, translate each one
            if isinstance(content.get(content_language, []), list):
                detected_language = detect_language(content.get(content_language, '')[0].get('content', ''))
                content[lang] = [
                    {
                        'title': translate_text(p.get('title', ''), lang),
                        'content': translate_text(p.get('content', ''), lang)
                    }
                    for p in content.get(detected_language, [])
                ]

        # Translate content conclusion
        if lang not in content_conclusion:
            detected_language = detect_language(content_conclusion.get(content_language, ''))
            content_conclusion[lang] = translate_text(content_conclusion.get(detected_language), lang)

    # Save the article data (assuming you have a serializer or model setup)
    article_data = {
        'title': title,
        'content_introduction': content_introduction,
        'content': content,
        'content_conclusion': content_conclusion,
        'created_by': request.user.id,
        'tags': data.get('tags', ''),
        'category': data.get('category', ''),
        'platform': data.get('platform', ''),
        'status': data.get('status', 'draft')
    }
    print('DATA TRANSLATION ----> OK')
    # Assuming you have an ArticleSerializer to validate and save the article
    serializer = ArticleSerializer(data=article_data)
    if serializer.is_valid():
        serializer.save()
        print('DATA SERIALIZATION ----> OK')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print('DATA SERIALIZATION ----> ERRORS')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






# API to upload article images
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])  # Ensure the parsers are applied here
def upload_article_image(request):
    print('request.data ---->',request.data)
    
    # Extract the article ID from the request
    article_id = request.data.get('article_id')
    
    try:
        article = Article.objects.get(id=article_id)
        # Use the serializer to validate and save the images
        data = request.data.copy()
        data['article'] = article.id  # Set the article ID in the image data
        data['created_by'] = request.user.id  # Set the current user as the image creator
        # Check if the file exists in the request
        if 'file' not in request.FILES:
            return Response({'error': 'No file was submitted.'}, status=status.HTTP_400_BAD_REQUEST)
        # Append the file from request.FILES
        data['image'] = request.FILES['file']
        data['category'] = request.data.get('category', 'thumbnail')  # Default to 'thumbnail' if not
        data['status'] = request.data.get('status', 'active')  # Default to 'active' if not provided
            
        # Serialize the data
        serializer = ArticleImageSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('serializer errors ---->',serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Article.DoesNotExist:
        return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)


# API to get all articles
@api_view(['GET'])
def get_articles(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


# API to get an article by ID
@api_view(['GET'])
def get_article(request, pk):
    try:
        article = Article.objects.get(id=pk)
        images = Article.objects.prefetch_related('images')  # Prefetch related images
        audios = Article.objects.prefetch_related('audios')  # Prefetch related audios 
        serialized_article = []
        
        # Serialize the article data
        article_serializer = ArticleSerializer(article).data
        
        # Fetch and serialize the associated images for the article
        images = ArticleImage.objects.filter(article=article)
        image_serializer = ArticleImageSerializer(images, many=True).data
        
        # Fetch and serialize the associated audios for the article
        audios = ArticleAudio.objects.filter(article=article)
        audio_serializer = ArticleAudioSerializer(audios, many=True).data
        # Add the images to the article data
        article_with_data = {
            **article_serializer,
            'images': image_serializer,
            'audios': audio_serializer
        }

        serialized_article.append(article_with_data)
        return Response(serialized_article, status=status.HTTP_200_OK)
    except Article.DoesNotExist:
        return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)
    
# API to get all images for an article
@api_view(['GET'])
def get_article_images(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        images = ArticleImage.objects.filter(article=article)
        serializer = ArticleImageSerializer(images, many=True)
        return Response(serializer.data)
    except Article.DoesNotExist:
        return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)
    

# API to get all articles with their images
@api_view(['GET'])
def get_articles_with_images(request):
    articles = Article.objects.prefetch_related('images')  # Prefetch related images
    audios = Article.objects.prefetch_related('audios')  # Prefetch related audios 
    serialized_articles = []

    for article in articles:
        # Serialize the article data
        article_serializer = ArticleSerializer(article).data
        
        # Fetch and serialize the associated images for the article
        images = ArticleImage.objects.filter(article=article)
        image_serializer = ArticleImageSerializer(images, many=True).data
        
        # Fetch and serialize the associated audios for the article
        audios = ArticleAudio.objects.filter(article=article)
        audio_serializer = ArticleAudioSerializer(audios, many=True).data
        # Add the images to the article data
        article_with_data = {
            **article_serializer,
            'images': image_serializer,
            'audios': audio_serializer
        }

        serialized_articles.append(article_with_data)
    
    return Response(serialized_articles, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # Require user authentication
def delete_article(request, pk):
    """
    Delete an article by ID.
    """
    try:
        # Fetch the article by ID or return 404 if not found
        article = get_object_or_404(Article, id=pk)

        # Optional: Check if the request user is the owner of the article or has permission to delete it
        if request.user != article.created_by and not request.user.is_staff:
            return Response({'error': 'You do not have permission to delete this article.'}, status=status.HTTP_403_FORBIDDEN)

        # Delete the article
        article.delete()

        # Return a success response
        return Response({'message': 'Article deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Article.DoesNotExist:
        return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)