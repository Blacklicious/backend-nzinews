# views.py
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Video
from ..serializers import VideoSerializer
from django.shortcuts import get_object_or_404



# Function-Based View for Video list
@api_view(['GET'])
def get_videos(request):
    """
    List all videos or create a new one.
    """
    if request.method == 'GET':
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)  # Serialize all Video objects
        return Response(serializer.data, status=status.HTTP_200_OK)
    



# API to get an article by ID
@api_view(['GET'])
def get_video(request, pk):
    try:
        video = Video.objects.get(id=pk)
        serialized_video = []      
        # Serialize the article data
        video_serializer = VideoSerializer(video).data
        serialized_video.append(video_serializer)
        return Response(serialized_video, status=status.HTTP_200_OK)
    except Video.DoesNotExist:
        return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)
    



# CREATE a new video (POST request)
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Authentication required
@parser_classes([MultiPartParser, FormParser])  # Enable handling of file uploads
def create_video(request):
    """
    Create a new video, but first check if a video with the same title and language exists.
    """
    # Extract data and files from the request
    data = request.data  # Form data (non-file fields)
    files = request.FILES  # File data (thumbnail, content, etc.)

    title_to_search = data.get('title')  # Title of the video
    language_to_search = data.get('language')  # Language of the video

    # Create a dictionary with all the required fields for the video model
    video_data = {
        'title': title_to_search,
        'description': data.get('description'),
        'tags': data.get('tags', ''),
        'category': data.get('category', ''),
        'publisher': data.get('publisher', ''),
        'platform': data.get('platform', ''),
        'language': language_to_search,
        'release_date': data.get('release_date'),
        'status': data.get('status', 'draft'),
        'created_by': request.user.id,  # Automatically set to the authenticated user
        'thumbnail': files.get('thumbnail'),  # Handle file upload for thumbnail
        'content': files.get('content'),  # Handle file upload for content (PDF)
        'link': data.get('link', '')
    }

    # Proceed to create the new video if no duplicate exists
    if request.method == 'POST':
        # Pass the video_data to the serializer
        serializer = VideoSerializer(data=video_data)
        if serializer.is_valid():
            serializer.save()  # Save the new video
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# UPDATE an existing video (PUT or PATCH request)
@api_view(['PUT', 'PATCH'])
def update_video(request, pk):
    """
    Update an existing video.
    """
    video = get_object_or_404(Video, pk=pk)  # Retrieve the video to update
    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'  # Allow partial updates with PATCH
        serializer = VideoSerializer(video, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()  # Save the updated video
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# DELETE an existing video (DELETE request)
@api_view(['DELETE'])
def delete_video(request, pk):
    """
    Delete a Video.
    """
    video = get_object_or_404(Video, pk=pk)  # Retrieve the Video to delete
    if request.method == 'DELETE':
        video.delete()  # Delete the Video
        return Response(status=status.HTTP_204_NO_CONTENT)