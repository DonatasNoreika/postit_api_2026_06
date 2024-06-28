from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.response import Response
from .models import Post, Comment, PostLike, CommentLike
from .serializers import PostSerializer, CommentSerializer, PostLikeSerializer, UserSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User

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


class CommentList(generics.ListCreateAPIView):
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, post=post)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        comment = Comment.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if comment.exists():
            return super().delete(request, *args, **kwargs)
        else:
            raise ValidationError('Negalima trinti svetimų komentarų!')

    def put(self, request, *args, **kwargs):
        comment = Comment.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if comment.exists():
            return super().put(request, *args, **kwargs)
        else:
            raise ValidationError('Negalima redaguoti svetimų komentarų!')


class PostLikeCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = PostLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return PostLike.objects.filter(post=post, user=user)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError("Jūs jau palikote patiktuką šiam pranešimui!")
        post = Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, post=post)
        # super().perform_create(serializer)

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("Jūs nepalikote patiktuko po šiuo pranešimu!")


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
