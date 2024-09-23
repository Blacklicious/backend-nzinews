# views.py
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Magazine
from ..serializers import MagazineSerializer
from django.shortcuts import get_object_or_404



# Function-Based View for Magazine list
@api_view(['GET'])
def get_magazines(request):
    """
    List all magazines or create a new one.
    """
    if request.method == 'GET':
        magazines = Magazine.objects.all()
        serializer = MagazineSerializer(magazines, many=True)  # Serialize all Magazine objects
        return Response(serializer.data, status=status.HTTP_200_OK)
    



# API to get an article by ID
@api_view(['GET'])
def get_magazine(request, pk):
    try:
        magazine = Magazine.objects.get(id=pk)
        serialized_magazine = []      
        # Serialize the article data
        magazine_serializer = MagazineSerializer(magazine).data
        serialized_magazine.append(magazine_serializer)
        return Response(serialized_magazine, status=status.HTTP_200_OK)
    except Magazine.DoesNotExist:
        return Response({'error': 'Magazine not found'}, status=status.HTTP_404_NOT_FOUND)
    



# CREATE a new magazine (POST request)
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Authentication required
@parser_classes([MultiPartParser, FormParser])  # Enable handling of file uploads
def create_magazine(request):
    """
    Create a new magazine, but first check if a magazine with the same title and language exists.
    """
    # Extract data and files from the request
    data = request.data  # Form data (non-file fields)
    files = request.FILES  # File data (thumbnail, content, etc.)

    title_to_search = data.get('title')  # Title of the magazine
    language_to_search = data.get('language')  # Language of the magazine

    # Create a dictionary with all the required fields for the Magazine model
    magazine_data = {
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
        'content': files.get('content')  # Handle file upload for content (PDF)
    }

    # Proceed to create the new magazine if no duplicate exists
    if request.method == 'POST':
        # Pass the magazine_data to the serializer
        serializer = MagazineSerializer(data=magazine_data)
        if serializer.is_valid():
            serializer.save()  # Save the new magazine
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# UPDATE an existing magazine (PUT or PATCH request)
@api_view(['PUT', 'PATCH'])
def update_magazine(request, pk):
    """
    Update an existing magazine.
    """
    magazine = get_object_or_404(Magazine, pk=pk)  # Retrieve the magazine to update
    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'  # Allow partial updates with PATCH
        serializer = MagazineSerializer(magazine, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()  # Save the updated magazine
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# DELETE an existing magazine (DELETE request)
@api_view(['DELETE'])
def delete_magazine(request, pk):
    """
    Delete a magazine.
    """
    magazine = get_object_or_404(Magazine, pk=pk)  # Retrieve the magazine to delete
    if request.method == 'DELETE':
        magazine.delete()  # Delete the magazine
        return Response(status=status.HTTP_204_NO_CONTENT)