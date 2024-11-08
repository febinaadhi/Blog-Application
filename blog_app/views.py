from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from blog_app.models import CustomUser, Post
from .serializers import CustomUserSerializer, PostSerializer
import logging

# Setting up loggers
info_logger = logging.getLogger('info_logger')
errors_logger = logging.getLogger('errors_logger')

class UserSignupView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'statuscode': status.HTTP_201_CREATED,
                'title': 'Success',
                'data': serializer.data,
                'errors': None,
                'message': 'User created successfully.',
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        response_data = {
            'statuscode': status.HTTP_400_BAD_REQUEST,
            'title': 'Bad Request',
            'data': '',
            'errors': serializer.errors,
            'message': 'User creation failed.',
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            response_data = {
                'statuscode': status.HTTP_200_OK,
                'title': 'Success',
                'data': {'username': user.username},
                'errors': None,
                'message': 'Login successful.',
            }
            return Response(response_data, status=status.HTTP_200_OK)
        response_data = {
            'statuscode': status.HTTP_401_UNAUTHORIZED,
            'title': 'Unauthorized',
            'data': '',
            'errors': {'error': 'Invalid credentials'},
            'message': 'Login failed.',
        }
        return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)


class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            response_data = {
                'statuscode': status.HTTP_201_CREATED,
                'title': 'Success',
                'data': serializer.data,
                'errors': None,
                'message': 'Post created successfully.',
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        response_data = {
            'statuscode': status.HTTP_400_BAD_REQUEST,
            'title': 'Bad Request',
            'data': '',
            'errors': serializer.errors,
            'message': 'Post creation failed.',
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class PostListView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        response_data = {
            'statuscode': status.HTTP_200_OK,
            'title': 'Success',
            'data': serializer.data,
            'errors': None,
            'message': 'Posts retrieved successfully.',
        }
        return Response(response_data, status=status.HTTP_200_OK)


class PostPublishView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk, author=request.user)
            post.is_published = True
            post.save()
            response_data = {
                'statuscode': status.HTTP_200_OK,
                'title': 'Success',
                'data': {'post_id': post.id, 'is_published': post.is_published},
                'errors': None,
                'message': 'Post published successfully.',
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            response_data = {
                'statuscode': status.HTTP_404_NOT_FOUND,
                'title': 'Not Found',
                'data': '',
                'errors': {"error": "Post does not exist or you do not have permission."},
                'message': 'Publish failed.',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            if request.user in post.likes.all():
                post.likes.remove(request.user)
                message = 'Post unliked successfully.'
            else:
                post.likes.add(request.user)
                message = 'Post liked successfully.'
            post.save()
            response_data = {
                'statuscode': status.HTTP_200_OK,
                'title': 'Success',
                'data': {'post_id': post.id, 'likes_count': post.likes.count()},
                'errors': None,
                'message': message,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            response_data = {
                'statuscode': status.HTTP_404_NOT_FOUND,
                'title': 'Not Found',
                'data': '',
                'errors': {"error": "Post does not exist"},
                'message': 'Like operation failed.',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
