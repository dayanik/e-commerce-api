from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from . import serializers


User = get_user_model()


class SignUpView(generics.CreateAPIView):
    queryset = User
    serializer_class = serializers.SignUpSerializer
    permission_classes = [AllowAny]
