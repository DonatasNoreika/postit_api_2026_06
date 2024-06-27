from django.shortcuts import render
from rest_framework import generics
from .models import Post, Comment, PostLike, CommentLike
from .serializers import PostSerializer

# Create your views here.

class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer