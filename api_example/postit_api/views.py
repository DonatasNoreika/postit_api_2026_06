from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Post, Comment, PostLike, CommentLike
from .serializers import PostSerializer
from rest_framework.exceptions import ValidationError

# Create your views here.

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if post.exists():
            return super().delete(request, *args, **kwargs)
        else:
            raise ValidationError("Negalima trinti svetimų pranešimų!")

    def put(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if post.exists():
            return super().put(request, *args, **kwargs)
        else:
            raise ValidationError("Negalima redaguoti svetimų pranešimų!")


