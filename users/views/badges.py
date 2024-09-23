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
from ..models import Member, Employee, Business, Badge
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer