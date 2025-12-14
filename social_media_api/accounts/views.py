from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import generics 
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, SimpleUserSerializer
from .models import CustomUser

User = get_user_model()


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
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"message": "Login successful", "token": token.key})
    return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(User, pk=user_id)
        actor = request.user
        if target == actor:
            return Response({'detail': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        if actor.is_following(target):
            return Response({'detail': 'Already following.'}, status=status.HTTP_400_BAD_REQUEST)
        actor.following.add(target)
        return Response({'detail': 'Followed successfully.'}, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(User, pk=user_id)
        actor = request.user
        if target == actor:
            return Response({'detail': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        if not actor.is_following(target):
            return Response({'detail': 'Not following.'}, status=status.HTTP_400_BAD_REQUEST)
        actor.following.remove(target)
        return Response({'detail': 'Unfollowed successfully.'}, status=status.HTTP_200_OK)




class FollowingListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SimpleUserSerializer

    def get_queryset(self):
        # ?user_id= optional to view another user's following list; default current user
        user_id = self.request.query_params.get('user_id')
        if user_id:
            user = get_object_or_404(User, pk=user_id)
        else:
            user = self.request.user
        return user.following.all()


class FollowersListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SimpleUserSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            user = get_object_or_404(User, pk=user_id)
        else:
            user = self.request.user
        return user.followers.all()


class UsersListView(generics.GenericAPIView):
    """View to list all users - demonstrates GenericAPIView usage and CustomUser.objects.all()"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SimpleUserSerializer
    
    def get_queryset(self):
        return CustomUser.objects.all()
    
    def get(self, request):
        queryset = CustomUser.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)