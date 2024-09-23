
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from ..serializers import UserSerializer, RegisterSerializer, MemberSerializer, EmployeeSerializer, BusinessSerializer, BadgeSerializer
from ..models import Member, Employee, Business, Badge
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_member(request):
    # Log the incoming data for debugging purposes
    print("Incoming data:", request.data)

    # Initialize the serializer with the request data and include the request context
    serializer = MemberSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        # Save the Member with the authenticated user automatically set
        serializer.save()
        # Log the created Member for debugging
        print("Member created:", serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        # Log errors if the data is not valid
        print("Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_member(request):
    try:
        member = Member.objects.get(user=request.user)
        serializer = MemberSerializer(member)
        return Response(serializer.data)
    except Member.DoesNotExist:
        return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_member(request):
    try:
        member = Member.objects.get(user=request.user)
    except Member.DoesNotExist:
        return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MemberSerializer(member, data=request.data, partial=True, context={'request': request})
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_member(request):
    try:
        member = Member.objects.get(user=request.user)
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Member.DoesNotExist:
        return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
