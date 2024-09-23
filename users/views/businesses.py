# users/views.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from ..serializers import BusinessSerializer, BusinessImageSerializer
from ..models import Business, BusinessImage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_business(request):
    # Log the incoming data and files for debugging purposes
    print("Incoming data:", request.data)
    print("Incoming files:", request.FILES)
    
    serializer = BusinessSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print("Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
def get_businesses(request):
    businesses = Business.objects.all()
    if businesses.exists():
        serializer = BusinessSerializer(businesses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'No businesses found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_business(request, pk):
    try:
        business = Business.objects.get(pk=pk)
        serializer = BusinessSerializer(business)
        return Response(serializer.data)
    except Business.DoesNotExist:
        return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_business(request, pk):
    try:
        business = Business.objects.get(pk=pk)
    except Business.DoesNotExist:
        return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BusinessSerializer(business, data=request.data, partial=True, context={'request': request})
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_business(request, pk):
    try:
        business = Business.objects.get(pk=pk)
        business.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Business.DoesNotExist:
        return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_business_image(request, pk):
    try:
        business = Business.objects.get(pk=pk)
    except Business.DoesNotExist:
        return Response({'error': 'Business not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BusinessImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(business=business)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)