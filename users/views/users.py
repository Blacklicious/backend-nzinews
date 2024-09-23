# users/views.py

from rest_framework import viewsets, status
from django.contrib.auth.models import User # type: ignore
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics # type: ignore
from rest_framework.permissions import AllowAny # type: ignore
from rest_framework_simplejwt.views import TokenObtainPairView # type: ignore
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # type: ignore
from ..serializers import UserSerializer, RegisterSerializer, MemberSerializer, EmployeeSerializer, BusinessSerializer, BadgeSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    try:
        # Directly use request.user
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
