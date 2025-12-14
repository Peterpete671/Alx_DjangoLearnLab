from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment
from accounts.serializers import SimpleUserSerializer
from .models import Like

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_picture']
        read_only_fields = ['id', 'username', 'profile_picture']


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)
    post_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'post_id', 'author', 'author_id', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
        extra_kwargs = {'post': {'read_only': True}}

    def create(self, validated_data):
        validated_data.pop('author_id', None)
        validated_data.pop('post_id', None)
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_id', 'title', 'content', 'created_at', 'updated_at', 'comments', 'comments_count']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'comments']

    def get_comments_count(self, obj):
        return obj.get_comments_count()

    def create(self, validated_data):
        validated_data.pop('author_id', None)
        return super().create(validated_data)

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()

    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value.strip()


class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'comments_count']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def get_comments_count(self, obj):
        return obj.get_comments_count()
    
class PostSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer

    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'created_at')

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'user', 'post', 'created_at')