from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, UserSerializer
from .models import User
# Create your views here.

@api_view(['POST'])
def register_user(request):
	serializer = RegisterSerializer(data=request.data)
	if serializer.is_valid():
		user = serializer.save()
		token = Token.objects.get(user=user)
		return Response({
			"message": "User registered successfully",
			"token": token.key
		}, status=status.HTTP_201_CREATED)

	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
	username = request.data.get("username")
	password = request.data.get("password")

	user = authenticate(username=username, password=password)

	if user is not None:
		token, created = Token.objects.get_or_create(user=user)
		return Response({
			"message": "Login successful",
			"token": token.key
		})
	else:
		return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_profile(request):
	user = request.user
	serializer = UserSerializer(user)
	return Response(serializer.data)
