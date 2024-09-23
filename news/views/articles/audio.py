from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from news.models import Article, ArticleAudio
from news.serializers import ArticleAudioSerializer
from google.cloud import texttospeech
from django.utils.text import slugify
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.conf import settings


# Function to generate audio using Google TTS
def generate_article_audio(content, language_code='en-US', voice_name='en-US-Wavenet-D', audio_format='MP3'):
    client = texttospeech.TextToSpeechClient(credentials=settings.GT_CREDENTIALS)
    input_text = texttospeech.SynthesisInput(text=content)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text,
        voice=voice,
        audio_config=audio_config
    )

    return response.audio_content

# Function to save audio to the ArticleAudio model
def save_article_audio(article, user, audio_content,audio_language):
    category_slug = slugify(article.category)
    audio_filename = f"{category_slug}-audio-{article.id}.mp3"
    
    audio_file = ContentFile(audio_content, name=audio_filename)

    article_audio = ArticleAudio(
        article=article,
        language=audio_language,
        category=article.category,
        created_by=user,
        status='active'
    )
    
    # Save the audio file to the audio field
    article_audio.audio.save(audio_filename, audio_file)
    article_audio.save()

    return article_audio

# API view to create audio for an article
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_article_audio(request, article_id):
    try:
        # Retrieve the article
        article = Article.objects.get(id=article_id)
        user = User.objects.get(id=1)  
        # Get language and content from request data
        audio_language = request.data.get('language', 'en')
        content = request.data.get('content', '')

        # Check if an audio file already exists for this article-language pair
        existing_audio = ArticleAudio.objects.filter(article=article, language=audio_language).first()
        if existing_audio:
            return Response({
                'error': f'Audio for this article in {audio_language} already exists.'
            }, status=status.HTTP_400_BAD_REQUEST)

        language_map = {
            'en': 'en-GB',    # British English
            'fr': 'fr-FR',    # French
            'es': 'es-ES',    # Spanish
            # Add more languages if needed
        }
        # Check if the language is supported
        laguage_name = language_map.get(audio_language, 'en-GB')  # Default to 'en-GB'
        # Map the language to the corresponding Google TTS voice
        voice_map = {
            'en': 'en-GB-Wavenet-A',    # British English voice
            'fr': 'fr-FR-Standard-B',   # French Standard voice
            'es': 'es-ES-Wavenet-A',    # Spanish voice
            # Add more languages and voices if needed
        }
        # Select the appropriate voice based on the language
        voice_name = voice_map.get(audio_language, 'en-GB-Wavenet-A')  # Default to 'en-GB-Wavenet-A'

        print(f"Generating audio for article: {article_id}")
        print(f"Content: {content}")
        print(f"Language: {laguage_name}")
        print(f"Voice: {voice_name}")

        # Generate audio using Google TTS
        audio_content = generate_article_audio(content, laguage_name, voice_name)

        # Save the audio file and associate it with the article
        article_audio = save_article_audio(article, user, audio_content, laguage_name)

        # Serialize the ArticleAudio instance
        serializer = ArticleAudioSerializer(article_audio)

        return Response({
            'message': 'Audio created successfully!',
            'audio': serializer.data
        }, status=status.HTTP_201_CREATED)

    except Article.DoesNotExist:
        return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# API view to get all article audios
@api_view(['GET'])
def get_article_audios(request):
    article_audios = ArticleAudio.objects.all()
    serializer = ArticleAudioSerializer(article_audios, many=True)
    return Response(serializer.data)
