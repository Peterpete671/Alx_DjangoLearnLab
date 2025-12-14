from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Post, Comment

User = get_user_model()


class PostModelTestCase(TestCase):
    """Test cases for Post model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_post_creation(self):
        """Test creating a post"""
        post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test content'
        )
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.author, self.user)
        self.assertEqual(str(post), f'Test Post by {self.user.username}')
    
    def test_post_comments_count(self):
        """Test getting comments count"""
        post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test content'
        )
        Comment.objects.create(
            post=post,
            author=self.user,
            content='Test comment'
        )
        self.assertEqual(post.get_comments_count(), 1)


class PostAPITestCase(APITestCase):
    """Test cases for Post API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123'
        )
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        
        self.post = Post.objects.create(
            author=self.user1,
            title='Test Post',
            content='Test content'
        )
    
    def test_list_posts_unauthenticated(self):
        """Test listing posts without authentication"""
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_post_authenticated(self):
        """Test creating a post with authentication"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        data = {
            'title': 'New Post',
            'content': 'New content'
        }
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
    
    def test_create_post_unauthenticated(self):
        """Test creating a post without authentication"""
        data = {
            'title': 'New Post',
            'content': 'New content'
        }
        response = self.client.post('/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_own_post(self):
        """Test updating own post"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        data = {'title': 'Updated Title'}
        response = self.client.patch(f'/api/posts/{self.post.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
    
    def test_update_other_user_post(self):
        """Test updating another user's post (should fail)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2.key}')
        data = {'title': 'Hacked Title'}
        response = self.client.patch(f'/api/posts/{self.post.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_own_post(self):
        """Test deleting own post"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.delete(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)
    
    def test_delete_other_user_post(self):
        """Test deleting another user's post (should fail)"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2.key}')
        response = self.client.delete(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_search_posts(self):
        """Test searching posts by title or content"""
        response = self.client.get('/api/posts/?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)


class CommentAPITestCase(APITestCase):
    """Test cases for Comment API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        self.token1 = Token.objects.create(user=self.user1)
        
        self.post = Post.objects.create(
            author=self.user1,
            title='Test Post',
            content='Test content'
        )
        
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user1,
            content='Test comment'
        )
    
    def test_create_comment(self):
        """Test creating a comment"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        data = {
            'post': self.post.id,
            'content': 'New comment'
        }
        response = self.client.post('/api/comments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_post_comments(self):
        """Test listing comments for a specific post"""
        response = self.client.get(f'/api/posts/{self.post.id}/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_filter_comments_by_post(self):
        """Test filtering comments by post"""
        response = self.client.get(f'/api/comments/?post={self.post.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
